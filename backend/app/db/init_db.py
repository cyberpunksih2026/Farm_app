from datetime import datetime, timezone, date
import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine, SessionLocal
import app.models
from app.models.user import User, UserRole
from app.models.farmer import Farmer, FarmerVerificationStatus
from app.models.category import Category
from app.models.product import Product, ProductUnit, ProductStatus
from app.models.inventory import Inventory
from app.models.setting import Setting
from app.core.security import get_password_hash

logger = logging.getLogger("farmapp.init_db")


def init_db(db: Optional[Session] = None) -> None:
    """
    Ensure all database tables exist and seed initial administrator, customer,
    employee, farmers from SIH26033, categories, products, and inventory.
    """
    logger.info("Verifying database schema and registering all FarmApp SQLAlchemy models...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified successfully.")

    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        now = datetime.now(timezone.utc)

        # 1. Seed Admin Account
        admin = db.query(User).filter(
            (User.username == "Admin") | (User.email == "ishanrajavelu75@gmail.com")
        ).first()
        if not admin:
            admin = User(
                username="Admin",
                full_name="FarmApp Administrator",
                email="ishanrajavelu75@gmail.com",
                phone="8110814178",
                password_hash=get_password_hash("Admin@123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_email_verified=True,
                created_at=now,
                updated_at=now
            )
            db.add(admin)
            logger.info("Created default Admin account (ishanrajavelu75@gmail.com / Admin@123)")
        else:
            admin.role = UserRole.ADMIN
            admin.is_active = True

        # 2. Seed Customer Account
        customer = db.query(User).filter(
            (User.username == "demo_customer") | (User.email == "customer@farmapp.in")
        ).first()
        if not customer:
            customer = User(
                username="demo_customer",
                full_name="Priya Sharma",
                email="customer@farmapp.in",
                phone="9876543210",
                password_hash=get_password_hash("Customer@123"),
                role=UserRole.CUSTOMER,
                is_active=True,
                is_email_verified=True,
                created_at=now,
                updated_at=now
            )
            db.add(customer)
            logger.info("Created demo Customer account (customer@farmapp.in / Customer@123)")

        # 3. Seed Employee / Delivery Account
        employee_user = db.query(User).filter(
            (User.username == "demo_employee") | (User.email == "delivery@farmapp.in")
        ).first()
        if not employee_user:
            employee_user = User(
                username="demo_employee",
                full_name="Karthik Delivery Partner",
                email="delivery@farmapp.in",
                phone="9876543211",
                password_hash=get_password_hash("Employee@123"),
                role=UserRole.EMPLOYEE,
                is_active=True,
                is_email_verified=True,
                created_at=now,
                updated_at=now
            )
            db.add(employee_user)
            logger.info("Created demo Employee account (delivery@farmapp.in / Employee@123)")

        db.flush()

        # 4. Seed Farmers (SIH26033 Integration)
        raw_farmers = [
            {"code": "F001", "name": "Farmer A", "location": "Villupuram", "lat": 11.9401, "lng": 79.4861, "bio": "Specializes in heirloom and vine-ripened tomatoes"},
            {"code": "F002", "name": "Farmer B", "location": "Cuddalore", "lat": 11.7480, "lng": 79.7714, "bio": "Organic red onion and shallot grower"},
            {"code": "F003", "name": "Farmer C", "location": "Tindivanam", "lat": 12.2340, "lng": 79.6550, "bio": "Heritage crop grower with sustainable drip irrigation"},
            {"code": "F004", "name": "Farmer D", "location": "Cuddalore", "lat": 11.7480, "lng": 79.7714, "bio": "High-yield golden potato and root tuber farm"},
            {"code": "F005", "name": "Farmer E", "location": "Puducherry", "lat": 11.9416, "lng": 79.8083, "bio": "Coastal micro-climate farm with certified organic tomatoes"},
            {"code": "F006", "name": "Farmer F", "location": "Villupuram", "lat": 11.9401, "lng": 79.4861, "bio": "Naturally dried red onion storage and farming"},
            {"code": "F007", "name": "Farmer G", "location": "Cuddalore", "lat": 11.7480, "lng": 79.7714, "bio": "Greenhouse cultivation of country tomatoes"},
            {"code": "F008", "name": "Farmer H", "location": "Tindivanam", "lat": 12.2340, "lng": 79.6550, "bio": "Large acreage tuber and potato cooperative member"},
            {"code": "F009", "name": "Farmer I", "location": "Villupuram", "lat": 11.9401, "lng": 79.4861, "bio": "Smallholder farmer cultivating fresh table tomatoes"},
            {"code": "F010", "name": "Farmer J", "location": "Puducherry", "lat": 11.9416, "lng": 79.8083, "bio": "Puducherry agro-cluster grower of sweet onions"}
        ]

        farmer_lookup = {}
        for f_data in raw_farmers:
            farmer = db.query(Farmer).filter(Farmer.farmer_code == f_data["code"]).first()
            if not farmer:
                farmer = Farmer(
                    farmer_code=f_data["code"],
                    name=f_data["name"],
                    phone=f"9100000{f_data['code'][-3:]}",
                    email=f"{f_data['code'].lower()}@farmapp.in",
                    location=f_data["location"],
                    state="Tamil Nadu" if f_data["location"] != "Puducherry" else "Puducherry",
                    latitude=f_data["lat"],
                    longitude=f_data["lng"],
                    farm_size_acres=5.5,
                    verification_status=FarmerVerificationStatus.VERIFIED,
                    is_active=True,
                    bio=f_data["bio"],
                    created_at=now,
                    updated_at=now
                )
                db.add(farmer)
                db.flush()
            farmer_lookup[f_data["code"]] = farmer

        # 5. Seed Categories
        categories_data = [
            {"name": "Fresh Vegetables", "slug": "vegetables", "description": "Farm fresh seasonal vegetables harvested daily", "icon": "Carrot", "order": 1},
            {"name": "Farm Fruits", "slug": "fruits", "description": "Naturally ripened orchard fruits with zero carbide", "icon": "Apple", "order": 2},
            {"name": "Root & Tubers", "slug": "tubers", "description": "Freshly unearthed potatoes, onions, and root crops", "icon": "Sprout", "order": 3},
            {"name": "Leafy Greens", "slug": "greens", "description": "Crisp pesticide-free spinach, coriander, and greens", "icon": "Leaf", "order": 4},
            {"name": "Dairy & Staples", "slug": "dairy", "description": "Farm-fresh milk, paneer, and authentic cold-pressed oils", "icon": "Milk", "order": 5}
        ]

        cat_lookup = {}
        for c_data in categories_data:
            cat = db.query(Category).filter(Category.slug == c_data["slug"]).first()
            if not cat:
                cat = Category(
                    name=c_data["name"],
                    slug=c_data["slug"],
                    description=c_data["description"],
                    icon=c_data["icon"],
                    display_order=c_data["order"],
                    is_active=True,
                    created_at=now,
                    updated_at=now
                )
                db.add(cat)
                db.flush()
            cat_lookup[c_data["slug"]] = cat

        # 6. Seed Products & Inventory
        products_data = [
            {
                "farmer_code": "F001",
                "cat_slug": "vegetables",
                "name": "Country Vine Tomatoes",
                "slug": "country-vine-tomatoes",
                "description": "Naturally sun-ripened country tomatoes from Villupuram with high lycopene and rich tang.",
                "unit": ProductUnit.KG,
                "farmer_price": 25.0,
                "base_price": 32.0,
                "market_price": 45.0,
                "is_organic": True,
                "stock": 500.0,
                "image_url": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500"
            },
            {
                "farmer_code": "F002",
                "cat_slug": "tubers",
                "name": "Organic Red Onions",
                "slug": "organic-red-onions",
                "description": "Freshly cured pungent red onions directly sourced from Cuddalore smallholder farms.",
                "unit": ProductUnit.KG,
                "farmer_price": 30.0,
                "base_price": 38.0,
                "market_price": 52.0,
                "is_organic": True,
                "stock": 800.0,
                "image_url": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=500"
            },
            {
                "farmer_code": "F003",
                "cat_slug": "vegetables",
                "name": "Tindivanam Heirloom Tomatoes",
                "slug": "tindivanam-heirloom-tomatoes",
                "description": "Rich heritage variety cultivated using traditional drip irrigation techniques.",
                "unit": ProductUnit.KG,
                "farmer_price": 26.0,
                "base_price": 34.0,
                "market_price": 46.0,
                "is_organic": False,
                "stock": 300.0,
                "image_url": "https://images.unsplash.com/photo-1546470427-e26264be0b11?w=500"
            },
            {
                "farmer_code": "F004",
                "cat_slug": "tubers",
                "name": "Cuddalore Golden Potatoes",
                "slug": "cuddalore-golden-potatoes",
                "description": "Thin-skinned versatile golden potatoes, perfect for daily curries and roasts.",
                "unit": ProductUnit.KG,
                "farmer_price": 22.0,
                "base_price": 28.0,
                "market_price": 40.0,
                "is_organic": False,
                "stock": 600.0,
                "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=500"
            },
            {
                "farmer_code": "F005",
                "cat_slug": "vegetables",
                "name": "Puducherry Coastal Tomatoes",
                "slug": "puducherry-coastal-tomatoes",
                "description": "Premium juicy tomatoes grown in nutrient-dense coastal soil with zero artificial chemicals.",
                "unit": ProductUnit.KG,
                "farmer_price": 27.0,
                "base_price": 35.0,
                "market_price": 48.0,
                "is_organic": True,
                "stock": 700.0,
                "image_url": "https://images.unsplash.com/photo-1561136594-7f68413baa99?w=500"
            },
            {
                "farmer_code": "F008",
                "cat_slug": "tubers",
                "name": "Tindivanam Sweet Potatoes",
                "slug": "tindivanam-sweet-potatoes",
                "description": "Rich orange-flesh sweet potatoes packed with vitamin A and natural goodness.",
                "unit": ProductUnit.KG,
                "farmer_price": 21.0,
                "base_price": 30.0,
                "market_price": 45.0,
                "is_organic": True,
                "stock": 900.0,
                "image_url": "https://images.unsplash.com/photo-1596097635121-14b63b7a0c19?w=500"
            },
            {
                "farmer_code": "F001",
                "cat_slug": "greens",
                "name": "Farm Fresh Palak Spinach",
                "slug": "farm-fresh-palak-spinach",
                "description": "Crisp tender spinach leaves harvested at sunrise to lock in nutrients.",
                "unit": ProductUnit.BUNCH,
                "farmer_price": 14.0,
                "base_price": 20.0,
                "market_price": 30.0,
                "is_organic": True,
                "stock": 180.0,
                "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=500"
            },
            {
                "farmer_code": "F005",
                "cat_slug": "fruits",
                "name": "GI Tagged Alphonso Mangoes",
                "slug": "gi-tagged-alphonso-mangoes",
                "description": "Handpicked premium Alphonso mangoes, naturally straw-ripened with intense aroma.",
                "unit": ProductUnit.KG,
                "farmer_price": 120.0,
                "base_price": 150.0,
                "market_price": 210.0,
                "is_organic": True,
                "stock": 350.0,
                "image_url": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500"
            }
        ]

        for p_data in products_data:
            product = db.query(Product).filter(Product.slug == p_data["slug"]).first()
            farmer = farmer_lookup.get(p_data["farmer_code"])
            category = cat_lookup.get(p_data["cat_slug"])

            if not product and farmer and category:
                product = Product(
                    farmer_id=farmer.id,
                    category_id=category.id,
                    name=p_data["name"],
                    slug=p_data["slug"],
                    description=p_data["description"],
                    unit=p_data["unit"],
                    base_price=p_data["base_price"],
                    farmer_price=p_data["farmer_price"],
                    market_price=p_data["market_price"],
                    image_url=p_data["image_url"],
                    is_organic=p_data["is_organic"],
                    harvest_date=date.today(),
                    status=ProductStatus.ACTIVE,
                    created_at=now,
                    updated_at=now
                )
                db.add(product)
                db.flush()

                # Add inventory record
                inventory = Inventory(
                    product_id=product.id,
                    stock_quantity=p_data["stock"],
                    reserved_quantity=0.0,
                    min_threshold=10.0,
                    unit=p_data["unit"],
                    last_restocked_at=now,
                    created_at=now,
                    updated_at=now
                )
                db.add(inventory)

        # 7. Seed Settings
        default_settings = [
            ("company_name", "FarmApp", "Company display name"),
            ("admin_notification_email", "ishanrajavelu75@gmail.com", "Primary administrator alert email"),
            ("free_delivery_threshold", "299", "Minimum cart value in INR for zero delivery fee"),
            ("standard_delivery_fee", "35", "Standard flat delivery fee in INR"),
            ("default_currency", "INR", "Standard billing currency code")
        ]

        for key, val, desc in default_settings:
            setting = db.query(Setting).filter(Setting.key == key).first()
            if not setting:
                db.add(Setting(key=key, value=val, description=desc))

        db.commit()
        logger.info("FarmApp database initialization & seeding completed successfully.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during database initialization: {e}", exc_info=True)
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    init_db()
