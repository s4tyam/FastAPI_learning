from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated, List
from sqlalchemy.orm import Session
import modles
from database import SessionLocal, engine
# CORS is always present in the FASTAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS USE
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

modles.Base.metadata.create_all(bind = engine)

@app.post("/transactions/", response_model= TransactionModel)
def create_transaction(transaction: TransactionBase, db: db_dependancy):
    db_transaction = modles.Transation(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found after creation")
    return db_transaction

@app.get("/transactions/", response_model= List[TransactionModel])
async def get_transaction(db: db_dependancy, skip: int = 0, limit: int = 100):
    transactions = db.query(modles.Transation).offset(skip).limit(limit).all()
    return transactions
