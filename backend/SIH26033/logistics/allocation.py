def allocate_supply(matched_farmers, required_quantity):
    """
    Allocate the buyer's requirement from matched farmers,
    starting with the nearest farmer.
    """
    if required_quantity <= 0:
        return [], 0

    collected = 0
    allocations = []

    for item in matched_farmers:
        farmer = item["farmer"]
        distance = item["distance"]

        remaining = required_quantity - collected
        allocation = min(farmer["quantity"], remaining)

        if allocation <= 0:
            continue

        allocations.append({
            "farmer_id": farmer["id"],
            "farmer_name": farmer["name"],
            "crop": farmer["crop"],
            "location": farmer["location"],
            "allocated_quantity": allocation,
            "distance": distance,
            "price": farmer["price"],
        })

        collected += allocation

        if collected >= required_quantity:
            break

    return allocations, collected
