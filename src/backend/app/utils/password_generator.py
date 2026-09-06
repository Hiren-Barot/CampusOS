import secrets
import string
import logging

logger = logging.getLogger(__name__)


def generate_temp_password(length: int = 12) -> str:
    if length < 8:
        length = 8
        logger.warning("Password length set to minimum 8 characters")
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special),
    ]
    
    all_chars = lowercase + uppercase + digits + special
    remaining_length = length - len(password)
    password.extend(secrets.choice(all_chars) for _ in range(remaining_length))
    
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def validate_password_strength(password: str) -> dict:
    result = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
    }
    
    if len(password) < 8:
        result["is_valid"] = False
        result["errors"].append("Password must be at least 8 characters long")
    elif len(password) < 12:
        result["warnings"].append("Password should be at least 12 characters for better security")
    
    if not any(c.isupper() for c in password):
        result["warnings"].append("Password should contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        result["warnings"].append("Password should contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        result["warnings"].append("Password should contain at least one digit")
    
    if not any(c in "!@#$%^&*" for c in password):
        result["warnings"].append("Password should contain at least one special character (!@#$%^&*)")
    
    return result