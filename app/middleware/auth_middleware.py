from fastapi import status, HTTPException, Depends

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.jwt_service import (decode_access_token)

from app.core.logger import logger


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:

        logger.error("JWT Validation failed")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    logger.info(f"TOKEN_VALIDATED | "
    f"user_id={payload.get('user_id')} | "
    f"role={payload.get('role')}")
    
    return payload