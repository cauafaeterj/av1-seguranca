# Documentação

Este projeto é uma API de autenticação, projetada para ser prática e eficiente, perfeita para quem quer entender como desenvolver um sistema de login protegido. A API foi desenvolvida com foco em segurança, usando várias camadas de proteção, como senhas criptografadas, verificação de IP, um código adicional de autenticação (segundo fator) registrado nos logs, e um CAPTCHA para tentativas incorretas. O objetivo foi criar algo claro e funcional, fácil de usar.

## Sobre a construção do projeto

A API foi construída utilizando o **Flask**, um framework leve e versátil que permite criar endpoints de forma rápida e adicionar camadas de segurança sem complicações. O sistema permite que usuários se cadastrem e façam login, com uma etapa extra de verificação usando um código de segundo fator. Para reforçar a proteção, as senhas são criptografadas com o algoritmo **SHA256**, e o IP do usuário é verificado em cada login. Caso a autenticação falhe, um CAPTCHA de 6 dígitos é gerado para impedir tentativas automáticas. O código de segundo fator, que em um ambiente real seria enviado por email, é aqui registrado no arquivo `log.txt` e exibido no console. Todas as ações importantes, como tentativas de login e cadastros, são gravadas nesse mesmo arquivo para monitoramento. O projeto utiliza o **SQLite** como banco de dados para armazenar os dados dos usuários de forma simples.

## Tecnologias utilizadas

- **Flask**: Framework principal para construir os endpoints da API (ex.: `/user/register` e `/user/login`) e gerenciar requisições HTTP.
- **Flask-SQLAlchemy**: Facilita a integração com o banco de dados SQLite, criando e gerenciando a tabela de usuários.
- **Flask-Login**: Gerencia sessões de usuários, mantendo o login ativo de forma segura após a autenticação.
- **Flask-Session**: Armazena temporariamente os códigos de CAPTCHA e segundo fator no servidor, usando sessões em arquivos.
- **Flask-CORS**: Permite que a API seja acessada por frontends em outros domínios, útil para testes.
- **Werkzeug**: Fornece a criptografia SHA256 para proteger as senhas dos usuários.

## Estrutura do projeto

O projeto foi organizado em arquivos e pastas para manter o código limpo e facilitar a manutenção:

- **Pasta** `app`: Contém os arquivos principais da API:
  - `controllers`: Arquivos que definem a lógica dos endpoints, como `auth_controller.py` (para cadastro e login), `user_controller.py` (para gerenciamento de usuários) e `validation.py` (para validação de dados).
  - `models`: Contém `user.py`, que define a estrutura da tabela de usuários no banco de dados.
  - `routes`: Arquivo `routes.py`, que mapeia os endpoints da API (ex.: `/user/register`).
  - `config.py`: Configurações gerais, como conexão com o banco de dados e a chave secreta para sessões.
  - `__init__.py`: Inicializa a aplicação Flask e configura as extensões.
- **Arquivos na raiz**:
  - `run.py`: Arquivo principal para executar a API.
  - `log.txt`: Registra ações como geração de CAPTCHA, códigos de segundo fator e tentativas de login.
  - `auth_api.db`: Banco de dados SQLite onde os dados dos usuários são armazenados.
  - `requirements.txt`: Lista as dependências do projeto.
  - `.env`: Arquivo com variáveis de ambiente, como a conexão com o banco de dados.
  - `.gitignore`: Define arquivos e pastas a serem ignorados pelo controle de versão.

Essa organização mantém o projeto modular e fácil de navegar, seguindo práticas recomendadas.

## Fluxo de Uso da API

Abaixo estão as URLs e os exemplos de JSON para cada etapa do processo de autenticação. Use ferramentas como Postman ou cURL para testar os endpoints.

### **Etapa 1: Cadastro de Usuário**

- **URL**: `POST http://localhost:8080/user/register`

- **Requisição**:

  ```json
  {
      "username": "maria",
      "password": "senha456",
      "nome": "Maria Oliveira",
      "email": "maria@email.com",
      "perfil": "user",
      "ip_autorizado": "127.0.0.1"
  }
  ```

- **Resposta (Sucesso)**:

  ```json
  {
      "message": "Usuário registrado com sucesso",
      "user": {
          "id": 1,
          "username": "maria",
          "nome": "Maria Oliveira",
          "email": "maria@email.com",
          "perfil": "user",
          "ip_autorizado": "127.0.0.1",
          "created_at": "2025-04-29T10:00:00"
      }
  }
  ```

### **Etapa 2: Login - Enviar Credenciais**

- **URL**: `POST http://localhost:8080/user/login`

- **Requisição**:

  ```json
  {
      "username": "maria",
      "password": "senha456"
  }
  ```

- **Resposta (Sucesso)**:

  ```json
  {
      "message": "Por favor, insira o CAPTCHA",
      "captcha_required": true,
      "captcha_code": "123456"
  }
  ```

### **Etapa 3: Login - Enviar CAPTCHA**

- **URL**: `POST http://localhost:8080/user/login`

- **Requisição**:

  - Use o `captcha_code` retornado na etapa anterior (ex.: "123456").

  ```json
  {
      "username": "maria",
      "password": "senha456",
      "captcha": "123456"
  }
  ```

- **Resposta (Sucesso)**:

  ```json
  {
      "message": "Por favor, insira o código do segundo fator",
      "second_factor_required": true,
      "second_factor_code": "654321"
  }
  ```

### **Etapa 4: Login - Enviar Segundo Fator**

- **URL**: `POST http://localhost:8080/user/login`

- **Requisição**:

  - Use o `second_factor_code` retornado na etapa anterior (ex.: "654321").

  ```json
  {
      "username": "maria",
      "password": "senha456",
      "captcha": "123456",
      "second_factor": "654321"
  }
  ```

- **Resposta (Sucesso)**:

  ```json
  {
      "message": "Login bem-sucedido",
      "user": {
          "id": 1,
          "username": "maria",
          "nome": "Maria Oliveira",
          "email": "maria@email.com",
          "perfil": "user",
          "ip_autorizado": "127.0.0.1",
          "created_at": "2025-04-29T10:00:00"
      }
  }
  ```

**Nota**: Consulte o arquivo `log.txt` para ver os códigos de CAPTCHA e segundo fator gerados, caso precise confirmar os valores.

## Como rodar o projeto

Siga os passos abaixo para configurar e executar a API:

1. **Crie e ative um ambiente virtual**:

   - No terminal, na raiz do projeto, crie o ambiente virtual:

     ```
     python -m venv venv
     ```

   - Ative o ambiente virtual:

     - No Windows:

       ```
       venv\Scripts\activate
       ```

     - No Linux/Mac:

       ```
       source venv/bin/activate
       ```

2. **Instale as dependências**:

   - Com o ambiente virtual ativado, instale as bibliotecas listadas no `requirements.txt`:

     ```
     pip install -r requirements.txt
     ```

3. **Configure as variáveis de ambiente**:

   - Crie ou edite o arquivo `.env` na raiz do projeto e adicione a conexão com o banco de dados etc..:

     ```
     DATABASE_URL=sqlite:///auth_api.db
     SECRET_KEY=sua_chave_secreta_aqui

     APP_HOST=127.0.0.1
     APP_PORT=8080
     FLASK_DEBUG=1
     ```

   - **Nota**: A `SECRET_KEY` deve ser uma string longa e aleatória. Você pode gerá-la com o comando:

     ```
     python -c "import secrets; print(secrets.token_hex(32))"
     ```

4. **Execute a API**:

   - Inicie o servidor Flask:

     ```
     python run.py
     ```

   - A API estará disponível em `http://localhost:8080`.

5. **Teste os endpoints**:

   - Use ferramentas como Postman ou cURL para testar os endpoints:
     - Cadastro: `POST http://localhost:8080/user/register`
     - Login: `POST http://localhost:8080/user/login`
   - Consulte o arquivo `log.txt` para ver os códigos de CAPTCHA e segundo fator gerados durante o processo de login.