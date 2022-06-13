from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
import datetime
from typing import List
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
def get_masters(db: Session, hinban: str, store: str):
	masters = db.query(models.Master).filter(
	        	and_(
	        		models.Master.hinban.contains(hinban),
	        		models.Master.store.contains(store)
	        	)
			).limit(500).all()
	return masters

def get_data(db: Session, day: str):
	data = db.query(models.Shuketu).filter(
				models.Shuketu.shuketubi == day
			).all()
	return data

# update
def update_data(db: Session, data: List[schemas.ShuketuGet]):
	try:
		for item in data:
			change_data = db.query(models.Shuketu).filter(models.Shuketu.id == item.id).one()
			change_data.ad = item.ad
			change_data.num = item.num
			change_data.num_all = item.num_all
			change_data.cust_name = item.cust_name
			change_data.due_date = item.due_date
			change_data.tonyu = item.tonyu
			change_data.inventory = item.inventory
			change_data.afure = item.afure
			change_data.shuketubi = item.shuketubi
			change_data.bin = item.bin
			change_data.comment = item.comment
			db.commit()
			db.refresh(change_data)
		return True
	except Exception as e:
		print(e)
		return False

# delete
def delete_data(db: Session, data: List[int]):
	try:
		for item in data:
			d_data = db.query(models.Shuketu).filter(models.Shuketu.id == item).one()
			db.delete(d_data)
			db.commit()
		return True
	except Exception as e:
		print(e)
		return False