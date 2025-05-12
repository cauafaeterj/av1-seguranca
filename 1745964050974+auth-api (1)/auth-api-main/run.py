from app import create_app

from dotenv import load_dotenv
import os


load_dotenv()

 
app = create_app()

if __name__ == "__main__":
    host = os.getenv('APP_HOST', '127.0.0.1')
    port = int(os.getenv('APP_PORT', '8081'))  
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
     
    app.run(host=host, port=port, debug=debug)
