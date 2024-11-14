# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, AdminLoginForm
import teste
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreta_chave'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Simulação de um banco de dados em memória para os usuários
# Admin login e senha são 'administrador@gmail.com' e '123'
users_db = {
    'administrador@gmail.com': {
        'password': '123',
        'name': 'Administrador',
        'is_admin': True
    },
}

class User(UserMixin):
    def __init__(self, email, name, is_admin=False):
        self.id = email
        self.name = name
        self.is_admin = is_admin

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user_data = users_db.get(user_id)
    if user_data:
        return User(email=user_id, name=user_data['name'], is_admin=user_data.get('is_admin', False))
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email in users_db:
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('login'))
        users_db[email] = {'password': password, 'name': form.name.data, 'is_admin': False}
        teste.cadastrar(form.name.data, email, password)
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        nome = teste.login(email, password)
        if nome:
            users_db[email] = {'password': password, 'name': nome, 'is_admin': False}
        user_data = users_db.get(email)
        if user_data :
            user = User(email=email, name=user_data['name'], is_admin=user_data.get('is_admin', False))
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        flash('Credenciais inválidas, tente novamente.', 'danger')
    return render_template('login.html', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Verifique se o e-mail é o do administrador e se a senha está correta
        admin_user = users_db.get('administrador@gmail.com')
        if admin_user and email == 'administrador@gmail.com' and password == '123':
            user = User(email='administrador@gmail.com', name='Administrador', is_admin=True)
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        
        flash('Credenciais de administrador inválidas.', 'danger')
    return render_template('admin_login.html', form=form)

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', user=current_user)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Acesso negado. Esta área é restrita a administradores.', 'danger')
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html', users=teste.allDB())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado com sucesso.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
