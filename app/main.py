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
  all_data = []
  for item in data:
    item_master = item.master
    buf = {
      'id': item.id,
      'ad': item.ad,
      's_num': item.num,
      'num_all': item.num_all,
      'cust_name': item.cust_name,
      'due_date': item.due_date,
      'tonyu': item.tonyu,
      'inventory': item.inventory,
      'afure': item.afure,
      'shuketubi': item.shuketubi,
      'bin': item.bin,
      'comment': item.comment,
      'sup_code': item_master.sup_code,
      'seban': item_master.seban,
      'hinban': item_master.hinban,
      'm_num': item_master.num,
      'store': item_master.store,
      'k_num': item_master.k_num,
      'y_num': item_master.y_num,
      'h_num': item_master.h_num
    }
    all_data.append(buf)
  return all_data

# update
@app.post('/data/update/')
async def update_data(data: List[schemas.ShuketuGet], db: Session=Depends(get_db)):
  if crud.update_data(db=db, data=data):
    return {
      'message':'update success'
    }
  else:
    return {
      'message':'error'
    }

# delete
@app.delete('/data/delete/')
async def delete_data(data: schemas.ShuketuGet, db: Session=Depends(get_db)):
  if crud.delete_data(db=db, data=data):
    return {
      'message':'delete success'
    }
  else:
    return {
      'message':'error'
    }