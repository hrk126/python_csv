from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
import datetime
from . import models, schemas

# create
def create_data(db: Session, data: schemas.ShuketuCreate):
  new_data = models.Shuketu(
    ad = data.ad,
    num = data.num,
    num_all = data.num_all,
    cust_name = data.cust_name,
    due_date = data.due_date,
    tonyu = data.tonyu,
    inventory = data.inventory,
    afure = data.afure,
    shuketubi = data.shuketubi,
    bin = data.bin,
    comment = data.comment
  )
  db.add(new_data)
  db.commit()
  db.refresh(new_data)
  return new_data

# read
# def get_master(db: Session, id: int):
#   re_master = db.query(models.Master).filter(models.Master.id == id).first()
#   return re_master

def get_masters(db: Session, hinban: str, store: str):
  masters = db.query(models.Master).filter(
              and_(
                models.Master.hinban.contains(hinban),
                models.Master.store.contains(store)
              )
            ).all()
  return masters

def get_data(db: Session, day: str):
  data = db.query(models.Shuketu).filter(
                models.Shuketu.shuketubi == day
            ).all()
  return data

# update
def update_data(db: Session, data: schemas.ShuketuGet):
    change_data = db.query(models.Shuketu).filter(models.Shuketu.id == data.id).first()
    change_data.ad = data.ad
    change_data.num = data.num
    change_data.num_all = data.num_all
    change_data.cust_name = data.cust_name
    change_data.due_date = data.due_date
    change_data.tonyu = data.tonyu
    change_data.inventory = data.inventory
    change_data.afure = data.afure
    change_data.shuketubi = data.shuketubi
    change_data.bin = data.bin
    change_data.comment = data.comment
    db.commit()
    db.refresh(change_data)
    return change_data

# delete
def delete_data(db: Session, data: schemas.ShuketuGet):
  try:
    d_data = db.query(models.Master).filter(models.Master.id == data.id).first()
    db.delete(d_data)
    db.commit()
    return True
  except:
    return False