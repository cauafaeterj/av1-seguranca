import logging
from flask import request, jsonify
from app import db
from app.models.user import User
from app.controllers.validation import sanitize_string, validate_email, validate_ip, validate_field

 
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  
)

class UserController:
    

    @staticmethod
    def register():
       
        data = request.get_json()
        if not data:
            logging.warning("Tentativa de registro sem dados fornecidos")
            return jsonify({"message": "Dados não fornecidos"}), 400

         
        username = sanitize_string(data.get('username'))
        password = sanitize_string(data.get('password'))
        nome = sanitize_string(data.get('nome'))
        email = data.get('email')  
        perfil = sanitize_string(data.get('perfil', 'user'))
        ip_autorizado = data.get('ip_autorizado') 

         
        required_fields = {'username': username, 'password': password, 'nome': nome, 'email': email}
        for field_name, value in required_fields.items():
            if value is None:
                logging.warning(f"Campo obrigatório ausente: {field_name}")
                return jsonify({"message": f"Campo obrigatório ausente: {field_name}"}), 400

         
        if not validate_field(username, "username", 50):
            return jsonify({"message": "Username inválido ou excede o tamanho máximo (50 caracteres)"}), 400
        if not validate_field(password, "password", 128):
            return jsonify({"message": "Senha inválida ou excede o tamanho máximo (128 caracteres)"}), 400
        if not validate_field(nome, "nome", 100):
            return jsonify({"message": "Nome inválido ou excede o tamanho máximo (100 caracteres)"}), 400
        if not validate_email(email):
            return jsonify({"message": "Formato de email inválido"}), 400
        if not validate_field(perfil, "perfil", 20):
            return jsonify({"message": "Perfil inválido ou excede o tamanho máximo (20 caracteres)"}), 400
        if not validate_ip(ip_autorizado):
            return jsonify({"message": "IP autorizado inválido"}), 400

         
        if User.query.filter_by(username=username).first():
            logging.warning(f"Tentativa de registro com username já existente: {username}")
            return jsonify({"message": "Username já registrado"}), 409
        if User.query.filter_by(email=email).first():
            logging.warning(f"Tentativa de registro com email já existente: {email}")
            return jsonify({"message": "Email já registrado"}), 409

         
        user = User(
            username=username,
            nome=nome,
            email=email,
            perfil=perfil,
            ip_autorizado=ip_autorizado
        )
        user.set_password(password)  

         
        try:
            db.session.add(user)
            db.session.commit()
            logging.info(f"Usuário registrado com sucesso: {username}")
            return jsonify({"message": "Usuário registrado com sucesso", "user": user.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao registrar usuário {username}: {str(e)}")
            return jsonify({"message": "Erro ao registrar usuário", "error": str(e)}), 500
