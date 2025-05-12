from flask import Blueprint
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController

 
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
     
    return UserController.register()

@user_bp.route('/login', methods=['POST'])
def login():
    
    return AuthController.login()
