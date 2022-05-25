from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Master(Base):
  __tablename__ = 'master'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  ad = Column(String, unique=True, index=True)
  sup_code = Column(String, ForeignKey('sup.sup_code', ondelete="SET NULL"), index=True)
  seban = Column(String, index=True)
  hinban = Column(String, index=True)
  num = Column(Integer, index=True)
  store = Column(String, index=True)
  k_num = Column(Integer, index=True)
  y_num = Column(Integer, index=True)
  h_num = Column(Integer, index=True)
  box = Column(String, index=True)
  shuketu = relationship('Shuketu', backref='master')

class Shuketu(Base):
  __tablename__ = 'shuketu'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  ad = Column(String, ForeignKey('master.ad', ondelete="SET NULL"), index=True)
  num = Column(Integer, index=True)
  num_all = Column(Integer, index=True)
  cust_name = Column(String, index=True)
  due_date = Column(String, index=True)
  tonyu = Column(Integer, index=True)
  inventory = Column(Integer, index=True)
  afure = Column(Integer, index=True)
  shuketubi = Column(String, index=True)
  bin = Column(Integer, index=True)
  comment = Column(String, index=True)
  
  class Sup(Base):
    __tablename__ = 'sup'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sup_code = Column(String, index=True)
    sup_name = Column(String, index=True)
    master = relationship('Master', backref='sup')
