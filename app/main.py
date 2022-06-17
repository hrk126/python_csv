# coding: cp932
from typing import List, Optional
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import datetime
import re

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
@app.get('/masters/')
async def get_masters(db: Session=Depends(get_db), hinban: str='', store: Optional[str]=''):
    masters = crud.get_masters(db=db, hinban=hinban, store=store)
    for master in masters:
        try:
            master.sup_name = master.sup.sup_name
        except Exception as e:
            master.sup_name = '不明'
            print(e)
        finally:
            delattr(master,'sup')
    return masters

# 集欠リストを返す
@app.get('/data/')
async def get_data(db: Session=Depends(get_db), day: str=datetime.date.today().isoformat()):
    data = crud.get_data(db=db, day=day)
    all_data = []
    for item in data:
        item_master = item.master
        master_sup = item_master.sup
        master_rui = item_master.rui
        d0 = '20' + master_rui.n_bi0
        d1 = '20' + master_rui.n_bi1
        d2 = '20' + master_rui.n_bi2
        # 内示
        n_0 = 0
        n_1 = 0
        n_2 = 0
        try:
            master_naiji = item_master.naiji
            n_0 = master_naiji.n0
            n_1 = master_naiji.n1
            n_2 = master_naiji.n2
        except Exception as e:
            print(e)
        # ストアキャパ
        store_capa = 0
        try:
            m = re.search(r'(TP|RG)(\d{3})', item_master.box)
            if m:
                box = 't' + m.group(2)
                master_capa = item_master.capa
                store_capa = getattr(master_capa, box) * master_capa.retu
        except Exception as e:
            print(e)
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
            'd0': d0[:4] + '-' + d0[4:6] + '-' + d0[6:],
            'hako0': master_rui.hako0,
            'd1': d1[:4] + '-' + d1[4:6] + '-' + d1[6:],
            'hako1': master_rui.hako1,
            'd2': d2[:4] + '-' + d2[4:6] + '-' + d2[6:],
            'hako2': master_rui.hako2,
            'n0': n_0,
            'n1': n_1,
            'n2': n_2,
            'capa': store_capa
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