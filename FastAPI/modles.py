from sqlalchemy import Column, Integer, Boolean, Float, String
from database import Base

class Transation(Base):
    __tablename__ = 'transations'
    id = Column(Integer, primary_key= True, index= True)
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    is_income = Column(Boolean)
    date = Column(String)