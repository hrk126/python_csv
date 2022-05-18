from typing import List, Optional
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# create
@app.post('/create/', response_model=schemas.ShuketuGet)
async def create_data(data: schemas.ShuketuCreate, db: Session=Depends(get_db)):
  return crud.create_data(db=db, data=data)

# read
# @app.get('/master/', response_model=schemas.MasterGet)
# async def get_master(db: Session=Depends(get_db), id: int=0):
#   re_master = crud.get_master(db=db, id=id)
#   return re_master

@app.get('/masters/', response_model=List[schemas.MasterGet])
async def get_masters(db: Session=Depends(get_db), hinban: str='', store: Optional[str]=''):
  masters = crud.get_masters(db=db, hinban=hinban, store=store)
  return masters

@app.get('/data/')
async def get_data(db: Session=Depends(get_db), day: str=datetime.date.today().isoformat()):
  data = crud.get_data(db=db, day=day)
  all_data = [item.master.hinban for item in data]
  return all_data

# update
@app.post('/data/update/', response_model=schemas.ShuketuGet)
async def update_data(data: schemas.ShuketuGet, db: Session=Depends(get_db)):
  return crud.update_data(db=db, data=data)

# delete
@app.delete('/data/delete')
async def delete_data(data: schemas.ShuketuGet, db: Session=Depends(get_db)):
  if crud.delete_data(db=db, data=data):
    return {
      'message':'delete success'
    }
  else:
    return {
      'message':'error'
    }