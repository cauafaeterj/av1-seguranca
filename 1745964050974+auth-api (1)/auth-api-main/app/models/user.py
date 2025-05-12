from app import db
from flask_login import UserMixin
from datetime import datetime
from Crypto.Hash import SHA256

class User(db.Model, UserMixin):
    

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)  
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  
    ip_autorizado = db.Column(db.String(45), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.today, nullable=False)

    def set_password(self, password):
        
        hash_obj = SHA256.new()
        hash_obj.update(password.encode('utf-8'))
        self.password_hash = hash_obj.hexdigest()

    def check_password(self, password):
         
        hash_obj = SHA256.new()
        hash_obj.update(password.encode('utf-8'))
        return self.password_hash == hash_obj.hexdigest()

    def to_dict(self):
        
        return {
            'id': self.id,
            'username': self.username,
            'nome': self.nome,
            'email': self.email,
            'perfil': self.perfil,
            'ip_autorizado': self.ip_autorizado,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        
        return f'<User {self.username}>'

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
