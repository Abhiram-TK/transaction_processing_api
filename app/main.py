from fastapi import FastAPI, Depends

from sqlalchemy import text

from app.api.transaction_routes import router

from app.core.logger import logger

from app.database.connection import engine, Base, SessionLocal

from app.middleware.auth_middleware import get_current_user

from app.models.transaction import Transaction

from app.services.jwt_service import decode_access_token

tags_metadata = [

    {"name": "Transactions", "description": "Transaction creation, retrieval, updates and business workflow processing."},

    {"name": "System", "description": "Service information and health monitoring."}]

app = FastAPI(title="Transaction Processing API", version="1.0.0", description=
              
              """Enterprise transaction management platform.

              Provides secure transaction processing, JWT authentication, RBAC authorization, rate limiting, idempotency protection, event-driven processing and 
              async validation.

              Integrated Services:
              - Authentication Service (Project 3)
              - PostgreSQL
              - Redis
              - Celery""", openapi_tags=tags_metadata,
              contact={"name": "Abhiram TK", "url": "https://github.com/Abhiram-TK", "email": "abhiramtksuresh@example.com"})

logger.info("Application initialized")

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["System"])
def home():

    return {"message": "Transaction Processing API Running"}

@app.get("/health", tags=["System"], summary="Health Check")
def health_check():

    db = SessionLocal()

    try:

        db.execute(text("SELECT 1"))

        return {"status": "healthy", "database": "connected"}

    except Exception:

        return {"status": "unhealthy", "database": "disconnected"}

    finally:

        db.close()