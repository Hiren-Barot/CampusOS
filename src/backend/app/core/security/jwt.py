from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
    ) -> str:
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRY_MINUTES)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    except Exception as e:
        logger.error(f"JWT creation error: {str(e)}")
        raise RuntimeError(f"Failed to create access token: {str(e)}")


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    
    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        return None
    
    except Exception as e:
        logger.error(f"Unexpected error during JWT decode: {str(e)}")
        return None