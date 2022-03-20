from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
  name: str
  code: int

class Item(ItemCreate):
  id: int

  class Config:
    orm_mode = True
