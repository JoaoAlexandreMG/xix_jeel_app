import os
from flask import Flask, render_template, redirect, url_for, request, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do app Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie_name'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Ativar apenas se estiver usando HTTPS

# Configuração do Auth0
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

# Inicializar o OAuth
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    authorize_url=f'https://{AUTH0_DOMAIN}/authorize',
    authorize_params=None,
    access_token_url=f'https://{AUTH0_DOMAIN}/oauth/token',
    refresh_token_url=f'https://{AUTH0_DOMAIN}/oauth/token',
    api_base_url=f'https://{AUTH0_DOMAIN}/api/v2/',
    client_kwargs={'scope': 'openid profile email'},
)

# Página inicial com o formulário de login
@app.route('/')
def index():
    return render_template('inscricao.html')

@app.route('/login')
def login():
    # Redireciona o usuário para o Auth0 para fazer login
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    # Verificar se o estado corresponde
    token = auth0.authorize_access_token()  # Obtém o token de acesso
    user = auth0.get('userinfo')  # Recupera as informações do usuário

    if user:
        session['user'] = user  # Armazena o usuário na sessão
        return redirect(url_for('profile'))  # Redireciona para a página protegida
    else:
        return redirect(url_for('index'))  # Redireciona para a página de login



# Página do usuário autenticado
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('index'))  # Se não estiver autenticado, redireciona para login

    user_info = session['user']
    return f"Olá, {user_info['name']}! Você está logado."

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))  # Redireciona para o login

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
