from flask import Blueprint
from app.routes.routes import user_bp

def register_routes(app):
    
    app.register_blueprint(user_bp, url_prefix='/user')
