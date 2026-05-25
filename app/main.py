from fastapi import FastAPI

from app.database.connection import engine
from app.database.connection import Base

from app.models.transaction import Transaction

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():

    return {"message": "Transaction Processing API Running"}

