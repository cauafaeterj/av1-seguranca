from flask import Blueprint
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController

# Cria um Blueprint para rotas relacionadas a usuários
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """Rota para registrar um novo usuário."""
    return UserController.register()

@user_bp.route('/login', methods=['POST'])
def login():
    """Rota para realizar login do usuário."""
    return AuthController.login()