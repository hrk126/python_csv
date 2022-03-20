from http.client import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

def get_items(db: Session, skip: int=0, limit=100):
  return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
  db_item = models.Item(name=item.name, code=item.code)
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item