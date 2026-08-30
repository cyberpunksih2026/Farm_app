from .distance import calculate_distance


def match_farmer_to_buyer(farmers, buyer):
    """
    Find farmers who have the requested crop and positive stock,
    calculate the prototype distance metric, and sort nearest first.
    """
    matched_farmers = []

    for farmer in farmers:
        if farmer["crop"].lower() != buyer["crop"].lower():
            continue

        if farmer["quantity"] <= 0:
            continue

        distance = calculate_distance(
            farmer["latitude"],
            farmer["longitude"],
            buyer["latitude"],
            buyer["longitude"],
        )

        matched_farmers.append({
            "farmer": farmer,
            "distance": distance,
        })

    matched_farmers.sort(key=lambda item: item["distance"])
    return matched_farmers
