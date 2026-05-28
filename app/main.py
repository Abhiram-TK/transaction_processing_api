from fastapi import FastAPI

from app.database.connection import engine
from app.database.connection import Base

from app.models.transaction import Transaction

from app.api.transaction_routes import router

from app.services.jwt_service import (create_access_token, decode_access_token)


app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():

    return {"message": "Transaction Processing API Running"}

