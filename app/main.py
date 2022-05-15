from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get('/', response_model=List[schemas.Item])
async def read_item(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
  items = crud.get_items(db=db, skip=skip, limit=limit)
  return items

@app.post('/', response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session=Depends(get_db)):
  return crud.create_item(db=db, item=item)