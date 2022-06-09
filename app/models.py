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
    rui = relationship('Rui', uselist=False)

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
    
class Rui(Base):
    __tablename__ = 'rui'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ad = Column(String, ForeignKey('master.ad', ondelete="CASCADE"), index=True, unique=True)
    n_bi0 = Column(String)
    n_bin0 = Column(String)
    h_kubun0 = Column(String)
    h_bi0 = Column(String)
    h_bin0 = Column(String)
    h_jikan0 = Column(String)
    noban0 = Column(String)
    hako0 = Column(Integer)
    nonyu0 = Column(Integer)
    n_bi1 = Column(String)
    n_bin1 = Column(String)
    h_kubun1 = Column(String)
    h_bi1 = Column(String)
    h_bin1 = Column(String)
    h_jikan1 = Column(String)
    noban1 = Column(String)
    hako1 = Column(Integer)
    nonyu1 = Column(Integer)
    n_bi2 = Column(String)
    n_bin2 = Column(String)
    h_kubun2 = Column(String)
    h_bi2 = Column(String)
    h_bin2 = Column(String)
    h_jikan2 = Column(String)
    noban2 = Column(String)
    hako2 = Column(Integer)
    nonyu2 = Column(Integer)
