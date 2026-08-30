# SIH26033 - Farmer-Buyer Logistics Prototype

This module demonstrates the Member 4/5 prototype:

- Farmer data
- Buyer/order data
- Crop matching
- Stock availability filtering
- Prototype distance calculation
- Nearest-first farmer ranking
- Supply allocation
- Structured logistics result
- Optional FastAPI endpoint

## Project structure

SIH26033/
├── main.py
├── day1.py
├── data/
│   ├── farmers.py
│   └── buyers.py
├── logistics/
│   ├── __init__.py
│   ├── distance.py
│   ├── matching.py
│   ├── allocation.py
│   └── logistics_engine.py
├── api/
│   ├── __init__.py
│   └── routes.py
├── requirements.txt
└── README.md

## 1. Install dependencies

Open the VS Code terminal inside this folder:

    python -m pip install -r requirements.txt

## 2. Run the Day-1 prototype

    python day1.py

The demo buyer needs 1000 kg of Tomato. The program selects suitable farmers,
starting from the nearest according to the prototype distance metric.

## 3. Run the FastAPI API

    python -m uvicorn main:app --reload

Then open the API documentation in a browser at:

    http://127.0.0.1:8000/docs

Use POST /api/logistics/match with JSON such as:

{
  "id": "B002",
  "name": "Demo Customer",
  "crop": "Tomato",
  "required_quantity": 1000,
  "location": "Puducherry",
  "latitude": 11.9416,
  "longitude": 79.8083
}

## Important prototype limitation

distance.py currently uses a simple coordinate-distance metric for learning and
demonstration. Its output is NOT kilometres and is NOT road distance.

For the final SIH system, replace this with a proper road-distance/routing
service or routing algorithm after the team decides the mapping stack.

## Integration note

This module is intended to be integrated with the team's main backend.
The team's authoritative inventory/database should eventually provide the
farmer and stock data rather than these demo Python lists.
