from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'supersecretkey'  # Substitua por uma chave secreta segura

mysql = MySQL(app)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página Home (apenas acessível se logado)
@app.route('/home')
def home():
    if 'logged_in' in session:
        username = session['username']
        return render_template('home.html', username=username, logged_in=True)
    else:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('index'))

# Rota para a página Features
@app.route('/features')
def features():
    return render_template('features.html')

# Rota para a página Pricing
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Rota para a página Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Rota para a página de cadastro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        flash('Cadastro realizado com sucesso! Faça login agora.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
