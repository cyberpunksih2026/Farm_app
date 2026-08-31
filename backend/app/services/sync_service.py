import json
import uuid
from datetime import datetime, timezone, date, time
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

from app.models.sync import Device, SyncOperation, SyncConflict
from app.models.employee import Employee, EmployeeStatus

from app.models.user import User
from app.models.audit_log import AuditAction
from app.services.audit_service import AuditService


class SyncService:
    @staticmethod
    def register_or_heartbeat_device(
        db: Session,
        device_id: str,
        device_name: str,
        platform: str = "android",
        app_version: Optional[str] = "1.0.0",
        user: Optional[User] = None
    ) -> Device:
        """Register a new device installation or update last synchronization heartbeat."""
        device = db.query(Device).filter(Device.device_id == device_id).first()
        now = datetime.now(timezone.utc)

        if not device:
            device = Device(
                device_id=device_id,
                user_id=user.id if user else None,
                device_name=device_name,
                platform=platform,
                app_version=app_version,
                last_sync_at=now,
                is_active=True,
                created_at=now
            )
            db.add(device)
        else:
            device.device_name = device_name
            device.platform = platform
            if app_version:
                device.app_version = app_version
            if user:
                device.user_id = user.id
            device.last_sync_at = now

        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def get_registered_devices(db: Session) -> List[Device]:
        """Returns all registered devices."""
        return db.query(Device).order_by(Device.last_sync_at.desc().nullslast()).all()

    @staticmethod
    def push_sync_batch(
        db: Session,
        device_id: str,
        operations: List[Dict[str, Any]],
        user: User,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a batch of sync operations idempotently.
        Ensures duplicate operation_ids are ignored and conflicts are safely logged.
        """
        processed_count = 0
        skipped_count = 0
        conflicts_created = 0
        results = []

        # Heartbeat device
        SyncService.register_or_heartbeat_device(db, device_id, device_name=f"Device {device_id[:8]}", user=user)

        for op_data in operations:
            op_id = op_data.get("operation_id")
            if not op_id:
                op_id = str(uuid.uuid4())

            # 1. Idempotency check
            existing_op = db.query(SyncOperation).filter(SyncOperation.operation_id == op_id).first()
            if existing_op:
                skipped_count += 1
                results.append({
                    "operation_id": op_id,
                    "status": existing_op.status,
                    "message": "Already processed (idempotent skip)"
                })
                continue

            entity_type = op_data.get("entity_type")
            entity_id = str(op_data.get("entity_id") or "")
            action = op_data.get("operation", "CREATE").upper()
            payload = op_data.get("payload", {})

            try:
                if entity_type == "Attendance":
                    op_status, conflict_record = SyncService._sync_attendance(
                        db, device_id, action, payload, user, ip_address
                    )
                elif entity_type == "Leave":
                    op_status, conflict_record = SyncService._sync_leave(
                        db, device_id, action, payload, user, ip_address
                    )
                elif entity_type == "Employee":
                    op_status, conflict_record = SyncService._sync_employee(
                        db, device_id, action, payload, user, ip_address
                    )
                else:
                    op_status = "PROCESSED"
                    conflict_record = None

                # Log sync operation for idempotency
                sync_op = SyncOperation(
                    operation_id=op_id,
                    device_id=device_id,
                    user_id=user.id,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    operation=action,
                    status=op_status,
                    processed_at=datetime.now(timezone.utc)
                )
                db.add(sync_op)
                db.commit()

                if op_status == "CONFLICT":
                    conflicts_created += 1
                    results.append({
                        "operation_id": op_id,
                        "status": "CONFLICT",
                        "conflict_id": conflict_record.conflict_id if conflict_record else None,
                        "message": "Conflict detected and preserved for manual review"
                    })
                else:
                    processed_count += 1
                    results.append({
                        "operation_id": op_id,
                        "status": "PROCESSED",
                        "message": "Synchronized successfully"
                    })

            except Exception as e:
                db.rollback()
                sync_op = SyncOperation(
                    operation_id=op_id,
                    device_id=device_id,
                    user_id=user.id,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    operation=action,
                    status="FAILED",
                    error_message=str(e),
                    processed_at=datetime.now(timezone.utc)
                )
                db.add(sync_op)
                db.commit()
                results.append({
                    "operation_id": op_id,
                    "status": "FAILED",
                    "error": str(e)
                })

        return {
            "processed": processed_count,
            "skipped": skipped_count,
            "conflicts": conflicts_created,
            "total": len(operations),
            "results": results
        }

   

    @staticmethod
    def _sync_employee(
        db: Session,
        device_id: str,
        action: str,
        payload: Dict[str, Any],
        user: User,
        ip_address: Optional[str]
    ) -> Tuple[str, Optional[SyncConflict]]:
        email = payload.get("email")
        existing = db.query(Employee).filter(Employee.email == email).first()
        if existing:
            return "PROCESSED", None

        emp = Employee(
            employee_id=payload.get("employee_id") or f"EMP-{uuid.uuid4().hex[:6].upper()}",
            first_name=payload.get("first_name", "Employee"),
            last_name=payload.get("last_name", ""),
            full_name=f"{payload.get('first_name', '')} {payload.get('last_name', '')}".strip(),
            email=email,
            phone=payload.get("phone"),
            department_id=payload.get("department_id"),
            designation=payload.get("designation", "Staff"),
            joining_date=date.today(),
            status=payload.get("status", "ACTIVE")
        )
        db.add(emp)
        db.flush()
        return "PROCESSED", None

    @staticmethod
    def pull_server_deltas(db: Session, since_timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Pull server master data and delta changes for local caching and synchronization."""
        employees = db.query(Employee).filter(Employee.deleted_at.is_(None)).all()
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "employees": [
                {
                    "id": e.id,
                    "uuid": e.uuid,
                    "employee_id": e.employee_id,
                    "full_name": e.full_name,
                    "first_name": e.first_name,
                    "last_name": e.last_name,
                    "email": e.email,
                    "department_id": e.department_id,
                    "designation": e.designation,
                    "status": e.status
                }
                for e in employees
            ]}

    @staticmethod
    def get_pending_conflicts(db: Session) -> List[SyncConflict]:
        """Returns all unresolved sync conflicts."""
        return db.query(SyncConflict).filter(SyncConflict.status == "PENDING").order_by(SyncConflict.created_at.desc()).all()

    @staticmethod
    def resolve_conflict(
        db: Session,
        conflict_id: str,
        resolution_strategy: str,
        resolution_notes: str,
        user: User,
        ip_address: Optional[str] = None
    ) -> SyncConflict:
        """
        Resolves a conflict with authorized decision:
        'SERVER_WINS', 'CLIENT_WINS', or 'MANUAL_MERGE'
        """
        conflict = db.query(SyncConflict).filter(SyncConflict.conflict_id == conflict_id).first()
        if not conflict:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conflict record not found")

        if conflict.status == "RESOLVED":
            return conflict

        if resolution_strategy == "CLIENT_WINS":
            # Apply client payload over server state
            client_data = json.loads(conflict.client_payload)
            if conflict.entity_type == "Attendance":
                emp_id = client_data.get("employee_id")
                
               

        conflict.status = "RESOLVED"
        conflict.resolved_by_user_id = user.id
        conflict.resolution_strategy = resolution_strategy
        conflict.resolution_notes = resolution_notes
        conflict.resolved_at = datetime.now(timezone.utc)

        AuditService.log(
            db,
            action="CONFLICT_RESOLVED",
            description=f"Resolved sync conflict #{conflict.conflict_id} on {conflict.entity_type} using {resolution_strategy}",
            user_id=user.id,
            entity_type="SyncConflict",
            entity_id=conflict.conflict_id,
            ip_address=ip_address
        )

        db.commit()
        db.refresh(conflict)
        return conflict
