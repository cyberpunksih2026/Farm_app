from .matching import match_farmer_to_buyer
from .allocation import allocate_supply


def create_result(buyer, allocations, collected):
    required = buyer["required_quantity"]
    fulfilled = collected >= required

    return {
        "buyer_id": buyer["id"],
        "buyer_name": buyer["name"],
        "crop": buyer["crop"],
        "required_quantity": required,
        "collected_quantity": collected,
        "shortage": max(required - collected, 0),
        "status": "fulfilled" if fulfilled else "shortage",
        "farmers": allocations,
    }


def process_order(farmers, buyer):
    """
    Main entry point for the logistics prototype.
    """
    if buyer["required_quantity"] <= 0:
        raise ValueError("required_quantity must be greater than 0")

    matched = match_farmer_to_buyer(farmers, buyer)
    allocations, collected = allocate_supply(
        matched,
        buyer["required_quantity"],
    )

    return create_result(buyer, allocations, collected)
