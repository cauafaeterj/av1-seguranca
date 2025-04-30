import logging
import random
from flask import request, jsonify, session
from flask_login import login_user
from app import db
from app.models.user import User
from app.controllers.validation import sanitize_string, validate_field

# Configuração do logging para salvar em log.txt com codificação UTF-8
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class AuthController:
    """Controlador para gerenciar operações de autenticação."""

    @staticmethod
    def login():
        """Realiza o login do usuário com autenticação, CAPTCHA, segundo fator e verificação de IP."""
        data = request.get_json()
        if not data:
            logging.warning("Tentativa de login sem dados fornecidos")
            return jsonify({"message": "Dados não fornecidos"}), 400

        # Sanitização e validação dos campos
        username = sanitize_string(data.get('username'))
        password = sanitize_string(data.get('password'))
        captcha_input = sanitize_string(data.get('captcha'))
        second_factor_input = sanitize_string(data.get('second_factor'))

        # Validação dos campos obrigatórios
        required_fields = {'username': username, 'password': password}
        for field_name, value in required_fields.items():
            if value is None:
                logging.warning(f"Campo obrigatório ausente: {field_name}")
                return jsonify({"message": f"Campo obrigatório ausente: {field_name}"}), 400

        # Validação de tipos e tamanhos
        if not validate_field(username, "username", 50):
            return jsonify({"message": "Username inválido ou excede o tamanho máximo (50 caracteres)"}), 400
        if not validate_field(password, "password", 128):
            return jsonify({"message": "Senha inválida ou excede o tamanho máximo (128 caracteres)"}), 400
        if captcha_input and not validate_field(captcha_input, "captcha", 6):
            return jsonify({"message": "CAPTCHA inválido ou excede o tamanho máximo (6 caracteres)"}), 400
        if second_factor_input and not validate_field(second_factor_input, "second_factor", 6):
            return jsonify({"message": "Código do segundo fator inválido ou excede o tamanho máximo (6 caracteres)"}), 400

        # Busca o usuário
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            logging.warning(f"Falha na autenticação: username={username}")
            return jsonify({"message": "Username ou senha inválidos"}), 401

        # Verificação do IP
        client_ip = request.remote_addr
        if user.ip_autorizado and user.ip_autorizado != client_ip:
            logging.warning(f"IP não autorizado para o usuário {username}: IP={client_ip}, IP Autorizado={user.ip_autorizado}")
            return jsonify({"message": "IP não autorizado"}), 403

        # Etapa 1: Gera o CAPTCHA se não houver entrada de CAPTCHA
        if not captcha_input:
            captcha_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            session[f'captcha_{username}'] = captcha_code  # Armazena na sessão
            logging.info(f"CAPTCHA gerado para o usuário {username}: {captcha_code}")
            return jsonify({"message": "Por favor, insira o CAPTCHA", "captcha_required": True, "captcha_code": captcha_code}), 200

        # Etapa 2: Valida o CAPTCHA
        stored_captcha = session.get(f'captcha_{username}')
        if not stored_captcha or captcha_input != stored_captcha:
            logging.warning(f"CAPTCHA incorreto para o usuário {username}: Inserido={captcha_input}, Esperado={stored_captcha}")
            # Limpa a sessão para evitar reutilização
            session.pop(f'captcha_{username}', None)
            session.pop(f'second_factor_{username}', None)
            return jsonify({"message": "CAPTCHA incorreto"}), 401

        # Etapa 3: Gera o segundo fator se o CAPTCHA for válido e não houver entrada de segundo fator
        if not second_factor_input:
            second_factor_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            session[f'second_factor_{username}'] = second_factor_code  # Armazena na sessão
            logging.info(f"Segundo fator de autenticação para o usuário {username}: {second_factor_code}")
            return jsonify({"message": "Por favor, insira o código do segundo fator", "second_factor_required": True, "second_factor_code": second_factor_code}), 200

        # Etapa 4: Valida o segundo fator
        stored_second_factor = session.get(f'second_factor_{username}')
        if not stored_second_factor or second_factor_input != stored_second_factor:
            logging.warning(f"Segundo fator incorreto para o usuário {username}: Inserido={second_factor_input}, Esperado={stored_second_factor}")
            # Limpa a sessão para evitar reutilização
            session.pop(f'captcha_{username}', None)
            session.pop(f'second_factor_{username}', None)
            return jsonify({"message": "Código do segundo fator incorreto"}), 401

        # Autentica o usuário com Flask-Login
        login_user(user)
        logging.info(f"Usuário {username} autenticado com sucesso")
        # Limpa a sessão após login bem-sucedido
        session.pop(f'captcha_{username}', None)
        session.pop(f'second_factor_{username}', None)
        return jsonify({"message": "Login bem-sucedido", "user": user.to_dict()}), 200