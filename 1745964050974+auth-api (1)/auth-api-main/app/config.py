import os

class Config:
    # Configuração do banco de dados SQLite
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não foi encontrada no ambiente. Verifique o arquivo .env.")
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração da SECRET_KEY para Flask-Session
    SECRET_KEY = os.getenv('SECRET_KEY')