from app import create_app

from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância da aplicação Flask
app = create_app()

if __name__ == "__main__":
    # Obtém configurações do .env, com valores padrão consistentes
    host = os.getenv('APP_HOST', '127.0.0.1')
    port = int(os.getenv('APP_PORT', '8081'))  
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # Inicia o servidor Flask
    app.run(host=host, port=port, debug=debug)