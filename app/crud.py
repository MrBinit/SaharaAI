from sqlalchemy.orm import Session
from app.models import Item
from app.database import SessionLocal

def get_items():
    db: Session = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

def create_item(name: str, description: str):
    db: Session = SessionLocal()
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return item