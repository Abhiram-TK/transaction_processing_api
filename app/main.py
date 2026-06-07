from fastapi import FastAPI, Depends

from app.database.connection import engine
from app.database.connection import Base

from app.models.transaction import Transaction

from app.api.transaction_routes import router

from app.services.jwt_service import decode_access_token

from app.middleware.auth_middleware import get_current_user

from app.core.logger import logger


app = FastAPI()

logger.info("Application initialized")

app.include_router(router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():

    return {"message": "Transaction Processing API Running"}