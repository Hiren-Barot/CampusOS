from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode('utf-8')
        
        return pwd_context.verify(plain_password, hashed_password)
    
    except ValueError as e:
        logger.error(f"Password verification error: {str(e)}")
        return False
    
    except Exception as e:
        logger.error(f"Unexpected error during password verification: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    try:
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        if len(password) > 72:
            logger.warning(f"Password length {len(password)} exceeds bcrypt 72-character limit. Truncating.")
            password = password[:72]
        
        return pwd_context.hash(password)
    
    except ValueError as e:
        logger.error(f"Password hashing error: {str(e)}")
        raise ValueError(f"Failed to hash password: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error during password hashing: {str(e)}")
        raise RuntimeError(f"Failed to hash password: {str(e)}")