from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session  
from app.config import Config


 
db = SQLAlchemy()
login_manager = LoginManager()
session = Session()  

def create_app():
    
    app = Flask(__name__)
    
     
    app.config.from_object(Config)
    
     
    app.config['SESSION_TYPE'] = 'filesystem'  
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'login_'
    
     
    db.init_app(app)
    login_manager.init_app(app)
    session.init_app(app)  
    CORS(app)

    
    login_manager.login_view = 'user.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

     
    with app.app_context():
        db.create_all()

    
    from app.routes import register_routes
    register_routes(app)
    
    return app
