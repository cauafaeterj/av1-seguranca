import re
import logging
import ipaddress

 
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  
)

def sanitize_string(value):
     
    if value is None:
        return None
    if not isinstance(value, str):
        logging.warning(f"Tentativa de sanitizar valor não-string: {value}")
        return None
     
    sanitized = ''.join(char for char in value.strip() if char.isprintable())
    if not sanitized:
        logging.warning(f"String sanitizada resultou em valor vazio: {value}")
    return sanitized

def validate_email(email):
 
    email = sanitize_string(email)
    if not email:
        logging.warning(f"Email inválido após sanitização: {email}")
        return False
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        logging.warning(f"Email inválido fornecido: {email}")
        return False
    if len(email) > 120:  
        logging.warning(f"Email excede o tamanho máximo (120 caracteres): {email}")
        return False
    logging.info(f"Email válido: {email}")
    return True

def validate_ip(ip):
     
    ip = sanitize_string(ip)
    if not ip:
        return True  
    try:
        ipaddress.ip_address(ip)
        if len(ip) > 45:  # Limite definido no modelo User
            logging.warning(f"IP excede o tamanho máximo (45 caracteres): {ip}")
            return False
        logging.info(f"IP válido: {ip}")
        return True
    except ValueError:
        logging.warning(f"IP inválido fornecido: {ip}")
        return False

def validate_field(value, field_name, max_length, allow_empty=False):
    
    if value is None and allow_empty:
        return True
    if not isinstance(value, str):
        logging.warning(f"Campo {field_name} não é uma string: {value}")
        return False
    value = sanitize_string(value)
    if not value and not allow_empty:
        logging.warning(f"Campo {field_name} está vazio após sanitização")
        return False
    if len(value) > max_length:
        logging.warning(f"Campo {field_name} excede o tamanho máximo ({max_length} caracteres): {value}")
        return False
    return True
