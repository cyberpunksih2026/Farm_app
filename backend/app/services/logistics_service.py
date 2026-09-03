import math
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.farmer import Farmer
from app.models.product import Product, ProductStatus
from app.models.inventory import Inventory
from app.schemas.logistics import BuyerRequest, FarmerAllocation, LogisticsResult


def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


class LogisticsService:
    @staticmethod
    def match_and_allocate_order(db: Session, buyer: BuyerRequest) -> LogisticsResult:
        crop_name = buyer.crop.strip().lower()
        required_qty = buyer.required_quantity

        if required_qty <= 0:
            raise ValueError("Required quantity must be greater than 0")

        products = db.query(Product).join(Product.farmer).join(Product.inventory).filter(
            Product.status == ProductStatus.ACTIVE,
            Farmer.is_active == True,
            (Product.name.ilike(f"%{crop_name}%")) | (Product.slug.ilike(f"%{crop_name}%"))
        ).all()

        matched_farmers: List[Dict[str, Any]] = []

        for p in products:
            inv: Inventory = p.inventory
            available_qty = inv.available_quantity if inv else 0.0
            if available_qty <= 0:
                continue

            farmer: Farmer = p.farmer
            dist = calculate_haversine_distance(
                farmer.latitude,
                farmer.longitude,
                buyer.latitude,
                buyer.longitude
            )

            matched_farmers.append({
                "farmer": farmer,
                "product": p,
                "available_quantity": available_qty,
                "distance": dist,
                "price": p.farmer_price
            })

        matched_farmers.sort(key=lambda item: item["distance"])

        allocations: List[FarmerAllocation] = []
        collected = 0.0

        for item in matched_farmers:
            remaining = required_qty - collected
            allocation = min(item["available_quantity"], remaining)

            if allocation <= 0:
                continue

            farmer = item["farmer"]
            unit_price = item["price"]
            total_cost = round(allocation * unit_price, 2)

            allocations.append(FarmerAllocation(
                farmer_id=farmer.id,
                farmer_code=farmer.farmer_code,
                farmer_name=farmer.name,
                crop=item["product"].name,
                location=farmer.location,
                allocated_quantity=round(allocation, 2),
                distance_km=item["distance"],
                price_per_kg=unit_price,
                total_cost=total_cost
            ))

            collected += allocation
            if collected >= required_qty:
                break

        fulfilled = collected >= required_qty
        shortage = max(0.0, required_qty - collected)

        return LogisticsResult(
            buyer_id=buyer.id,
            buyer_name=buyer.name,
            crop=buyer.crop,
            required_quantity=required_qty,
            collected_quantity=round(collected, 2),
            shortage=round(shortage, 2),
            status="fulfilled" if fulfilled else "shortage",
            total_farmers_matched=len(allocations),
            farmers=allocations
        )
