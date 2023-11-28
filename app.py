import os
from flask_cors import CORS
from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from alert import web  # Importe o módulo web.py

app = Flask(__name__)
CORS(app)

# Configurar o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Especificar o endpoint da página de login

# Definir a chave secreta a partir da variável de ambiente ou usar um valor padrão
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'defesa199')

# Modelo básico de usuário
class User(UserMixin):
    def __init__(self, username, password, role):
        self.id = username
        self.password = password
        self.role = role

# Lista de usuários (substitua por um banco de dados em um ambiente de produção)
users = {
    'defesa': User('defesa', '123', 'admin'),
    'compdec': User('compdec', '123', 'user')
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = users.get(nome)

    if user and user.password == senha:
        login_user(user)
        return redirect('/indexcomp') if user.role == 'user' else redirect('/index')
    else:
        error = "Senha incorreta. Tente novamente."
        return render_template('login.html', error=error)

@app.route('/indexcomp')
@login_required
def mapa_comp():
    if current_user.role == 'user':
        # Renderizar a página de mapa para usuários comuns
        return render_template('indexcomp.html')
    else:
        return redirect('/index')  # Redirecionar usuários não autorizados

@app.route('/index')
@login_required
def pagina():
    return render_template('pagina-incial.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dados')
@login_required
def dados():
    return render_template('dados.html')

@app.route('/mapa')  # Rota ajustada para /mapas
def mapa():
    return render_template('mapa.html')

# Adicione uma nova rota para chamar a função do web.py
@app.route('/disparar_alerta_web', methods=['POST'])
def disparar_alerta_web():
    try:
        print('Chamando obter_dados_do_navegador...')
        # from alert.web import obter_dados_do_navegador, verificar_enviar_email
        # dados_do_navegador = obter_dados_do_navegador()
        
        print('Chamando verificar_enviar_email...')
        # verificar_enviar_email(dados_do_navegador)

        return jsonify({'message': 'Alerta disparado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == "__main__":
    app.run(debug=True)
