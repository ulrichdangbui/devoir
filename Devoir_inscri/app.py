from flask import Flask, request, render_template, redirect, url_for
from Traitement import User
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page_sign', methods=['GET', 'POST'])
def register():
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if not name or not surname or not email or not password or not password2:
        error = "Tous les champs sont requis."
    elif "@gmail.com" not in email:
        error = "Vérifier bien votre adresse et que ce soit pour vous !."
    elif password != password2:
        error = "Les mots de passe ne correspondent pas."
    else:
        conn = psycopg2.connect('dbname=dbconn user=postgres password=mot_de_passe port=5432')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, surname, email, password) VALUES (?, ?, ?, ?)", (name, surname, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    render_template('page_sign.html', error=error)

@app.route('/index', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = psycopg2.connect('dbname=dbconn user=postgres password=mot_de_passe port=5432')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? and password=?", (email, password))
    user = c.fetchone()
    conn.close()
    if user:
        return redirect(url_for('home_page'))
    else:
        error = "Les informations pour se connecter sont incorrectes."
    return render_template('page_sign.html', error=error)

@app.route('/home_page')
def dashboard():
    return render_template('home_page.html')

if __name__ == '__main__':
    app.run(debug=True)
