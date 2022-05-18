from pydantic import BaseModel, Field


class MasterCreate(BaseModel):
  ad: str
  sup_code: str
  seban: str
  hinban: str
  num: int
  store: str
  k_num: int
  y_num: int
  h_num: int

class MasterGet(MasterCreate):
  id: int

  class Config:
    orm_mode = True


class ShuketuCreate(BaseModel):
  ad: str
  num: int
  num_all: int
  cust_name: str
  due_date: str
  tonyu: int
  inventory: int
  afure: int
  shuketubi: str
  bin: int
  comment: str

class ShuketuGet(ShuketuCreate):
  id: int

  class Config:
    orm_mode = True