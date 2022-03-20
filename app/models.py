from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .database import Base

class Item(Base):
  __tablename__ = 'items'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  name = Column(String, unique=True, index=True)
  code = Column(Integer, index=True)
