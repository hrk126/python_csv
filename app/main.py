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

@app.get('/masters/')
async def get_masters(db: Session=Depends(get_db), hinban: str='', store: Optional[str]=''):
  masters = crud.get_masters(db=db, hinban=hinban, store=store)
  for master in masters:
    try:
      master.sup_name = master.sup.sup_name
    except:
      master.sup_name = ''
      print('error')
    finally:
      delattr(master,'sup')
  return masters

@app.get('/data/')
async def get_data(db: Session=Depends(get_db), day: str=datetime.date.today().isoformat()):
  data = crud.get_data(db=db, day=day)
  all_data = []
  for item in data:
    item_master = item.master
    master_sup = item_master.sup
    buf = {
      'id': item.id,
      'ad': item.ad,
      'shuketubi': item.shuketubi,
      'bin': item.bin,
      'hinban': item_master.hinban,
      's_num': item.num,
      'num_all': item.num_all,
      'm_num': item_master.num,
      'box': item_master.box,
      'cust_name': item.cust_name,
      'due_date': item.due_date,
      'store': item_master.store,
      'tonyu': item.tonyu,
      'sup_code': item_master.sup_code,
      'sup_name': master_sup.sup_name,
      'seban': item_master.seban,
      'k_num': item_master.k_num,
      'y_num': item_master.y_num,
      'inventory': item.inventory,
      'afure': item.afure,
      'h_num': item_master.h_num,
      'comment': item.comment,
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

# delete
@app.post('/data/delete/')
async def delete_data(data: List[int], db: Session=Depends(get_db)):
  if crud.delete_data(db=db, data=data):
    return {
      'message':'delete success'
    }