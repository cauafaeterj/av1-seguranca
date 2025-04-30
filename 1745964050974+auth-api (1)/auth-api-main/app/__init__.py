from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session  
from app.config import Config


# Inicializa extensões globalmente
db = SQLAlchemy()
login_manager = LoginManager()
session = Session()  

def create_app():
    """Factory function para criar e configurar a aplicação Flask."""
    app = Flask(__name__)
    
    # Carrega configurações da classe Config
    app.config.from_object(Config)
    
    # Configurações do Flask-Session
    app.config['SESSION_TYPE'] = 'filesystem'  
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'login_'
    
    # Inicializa extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)
    session.init_app(app)  
    CORS(app)

    # Configura o LoginManager
    login_manager.login_view = 'user.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Cria as tabelas do banco no contexto da aplicação
    with app.app_context():
        db.create_all()

    # Importa e registra os Blueprints de rotas
    from app.routes import register_routes
    register_routes(app)
    
    return app