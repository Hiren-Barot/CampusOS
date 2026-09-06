import re
from datetime import datetime
from typing import Optional


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
  
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    
    return cleaned.isdigit() and len(cleaned) >= 10 and len(cleaned) <= 15


def validate_date_format(date_str: str) -> bool:
   
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_enum_value(value: str, allowed_values: list) -> bool:
   
    return value in allowed_values


def sanitize_string(input_str: str) -> str:
   
    dangerous_chars = ['<', '>', '"', "'", ';', '=', '\\', '/']
    for char in dangerous_chars:
        input_str = input_str.replace(char, '')
    
    input_str = input_str.strip()
    
    return input_str


def truncate_text(text: str, max_length: int = 200) -> str:
   
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."