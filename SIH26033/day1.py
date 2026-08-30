from data.farmers import farmers
from data.buyers import buyers
from logistics.logistics_engine import process_order


def print_result(result):
    print()
    print("=" * 55)
    print("       SIH FARMER-BUYER LOGISTICS DEMO")
    print("=" * 55)

    print()
    print("Buyer:", result["buyer_name"])
    print("Crop:", result["crop"])
    print("Required:", result["required_quantity"], "kg")
    print("Collected:", result["collected_quantity"], "kg")

    print()
    print("-" * 55)
    print("SELECTED FARMERS")
    print("-" * 55)

    if not result["farmers"]:
        print("No suitable farmers found.")
    else:
        for item in result["farmers"]:
            print()
            print("Farmer ID:", item["farmer_id"])
            print("Farmer:", item["farmer_name"])
            print("Location:", item["location"])
            print("Allocated:", item["allocated_quantity"], "kg")
            print("Demo distance:", round(item["distance"], 6))
            print("Price:", f"₹{item['price']}")

    print()
    print("-" * 55)

    if result["status"] == "fulfilled":
        print("Status: REQUIREMENT FULFILLED")
    else:
        print("Status: SUPPLY SHORTAGE")
        print("Shortage:", result["shortage"], "kg")

    print("-" * 55)


if __name__ == "__main__":
    buyer = buyers[0]
    result = process_order(farmers, buyer)
    print_result(result)
