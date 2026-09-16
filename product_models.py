from sqlalchemy import create_engine, String, FLOAT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional
from datetime import datetime

# --- Engine: connects to SQLite database file ---
engine = create_engine(
    "sqlite:///product_catalog.db",
    echo=True  
)

# Base class: 
class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories" # Table Name in database

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(300)) 

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}')"

    
class Product(Base):
    __tablename__ = "products" # Table Name in database

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(FLOAT, nullable=False)
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_name: Mapped[str] = mapped_column(String(50)) 

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}')"

Base.metadata.create_all(engine)
print("\\nTables created successfully!")


# Create Sessions

with Session(engine) as session:
    electronics = Category(name="Electronics", description="Electronic device")
    furniture = Category(name="Furniture", description="Home furniture")
    landscaping = Category(name="Landscaping", description="Garden product")

    session.add_all([electronics, furniture, landscaping])

    laptop = Product(
        name="Macbook Air",
        price=339.99,
        in_stock=True,
        category_name="Electronics"
    )

    camera = Product(
        name="Nikon 5",
        price=499.99, 
        in_stock=True,
        category_name="Electronics" 
    )

    chair = Product(
        name="Recline Folding Chair",
        price=69.99, 
        in_stock=True,
        category_name="Furniture" 
    )
    desk = Product(
        name="Pioneer Standing Desk",
        price=299.99, 
        in_stock=True,
        category_name="Furniture" 
    )
    rake = Product(
        name="Husky Heavy Duty Rake",
        price=39.99, 
        in_stock=True,
        category_name="Landscaping" 
    )

    shovel = Product(
        name="Husky Shovel",
        price=25.99,
        in_stock=True,
        category_name="Landscaping"
    )

    # Add to session
    session.add_all([laptop, camera, chair, desk, rake, shovel])

    session.commit()

    print(f"\\nCreated: {laptop}")
    print(f"Created: {camera}")
    print(f"Created: {chair}")
    print(f"Created: {desk}")
    print(f"Created: {rake}")
    print(f"Created: {shovel}")

# Get all Categories 
with Session(engine) as session: 
    print("\n=== All Categories ===")
    categories = session.query(Category).all()

    for category in categories: 
        print(category)

# All products in stock
with Session(engine) as session: 
    print("\n=== All Producst In Stock ===")
    products = session.query(Product).filter_by(in_stock=True).all()

    for product in products:
        print(product)



with Session(engine) as session: 
    print("\n=== Products Under $50 ===")
    cheap_products = session.query(Product).filter(Product.price < 50).all()

    for product in cheap_products:
        print(product)


                               
