from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import Config
import random
import string

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

mysql = MySQL(app)

# Função para gerar URL curta aleatória
def generate_short_url(original_url):
    url_name = original_url.rstrip('/').rsplit('/', 1)[-1][:3]  # Pegue os primeiros 3 caracteres da URL original
    random_part = ''.join(random.choices(string.digits, k=3))   # Adicione 3 números aleatórios
    return f"{url_name}{random_part}"

# Rota para redirecionar URL encurtada
@app.route('/<short_url>')
def redirect_to_url(short_url):
    cur = mysql.connection.cursor()
    cur.execute("SELECT original_url FROM urls WHERE short_url = %s", (short_url,))
    result = cur.fetchone()
    if result:
        # Incrementa o contador de cliques e insere no banco de dados de cliques
        cur.execute("UPDATE urls SET click_count = click_count + 1 WHERE short_url = %s", (short_url,))
        cur.execute("INSERT INTO clicks (url_id, user_id) VALUES ((SELECT id FROM urls WHERE short_url = %s), %s)", (short_url, session['user_id']))
        mysql.connection.commit()
        cur.close()
        return redirect(result[0])
    else:
        flash('URL encurtada não encontrada.', 'danger')
        return redirect(url_for('index'))

# Rota principal (página inicial)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página home
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'logged_in' in session:
        user_id = session['user_id']
        username = session['username']
        if request.method == 'POST':
            original_url = request.form['original_url']
            cur = mysql.connection.cursor()
            try:
                # Insere a URL apenas se ela não existir para o usuário
                cur.execute("SELECT short_url FROM urls WHERE original_url = %s AND user_id = %s", (original_url, user_id))
                existing_short_url = cur.fetchone()
                if existing_short_url:
                    short_url = existing_short_url[0]
                    flash(f'URL encurtada já existente: {request.url_root}{short_url}', 'info')
                else:
                    short_url = generate_short_url(original_url)
                    cur.execute("""
                        INSERT INTO urls (original_url, short_url, user_id)
                        VALUES (%s, %s, %s)
                    """, (original_url, short_url, user_id))
                    mysql.connection.commit()
                    flash(f'URL encurtada: {request.url_root}{short_url}', 'success')
            except Exception as e:
                flash(f'Erro ao encurtar a URL: {e}', 'danger')
            cur.close()
        
        # Obtém as URLs encurtadas do usuário logado
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, original_url, short_url, click_count FROM urls WHERE user_id = %s", (user_id,))
        urls = cur.fetchall()
        cur.close()
        
        return render_template('home.html', username=username, logged_in=True, urls=urls)
    else:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('index'))

# Rota para a página de recursos (features)
@app.route('/features')
def features():
    return render_template('features.html')

# Rota para a página de preços (pricing)
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Rota para a página de contato
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# Rota para o registro de usuário
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
            session['user_id'] = user[0]  # Acessa o ID do usuário na posição 0 da tupla
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))  # Redireciona para a página home
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
