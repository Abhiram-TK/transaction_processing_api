from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.core.config import settings

def decode_access_token(token: str):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload

    except JWTError:
        return None