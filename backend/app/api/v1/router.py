from fastapi import APIRouter
from app.api.v1 import (
    auth,
    users,
    farmers,
    categories,
    products,
    inventory,
    cart,
    orders,
    payments,
    delivery,
    logistics,
    notifications,
    ai,
    audit,
    settings,
    health,
    sync,
    system
)

api_router = APIRouter()

# Health endpoints mounted at root of api_router as well
api_router.include_router(health.router)

# Resource endpoints
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(farmers.router)
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(inventory.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)
api_router.include_router(delivery.router)
api_router.include_router(logistics.router)
api_router.include_router(notifications.router)
api_router.include_router(ai.router)
api_router.include_router(audit.router)
api_router.include_router(settings.router)
api_router.include_router(sync.router)
api_router.include_router(sync.devices_router)
api_router.include_router(system.router)
