from urllib.parse import quote_plus
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,redirect,url_for

app = Flask(__name__)
password = quote_plus('mot_de_passe')
database_name = 'dbconn'
conn = 'postgresql://postgres:{}@localhost:5432/{}'.format(password,database_name)
app.config["SQLALCHEMY_DATABASE_URI"] = conn
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

def enregi_user(name, surname, email, password):
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    enregi_user(name, surname, email, password)
    user = User(name=name, surname=surname, email=email, password=password)
    db.session.add(user)
    db.session.commit()

def crypt_pass(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return redirect(url_for('home_page'))
    else:
        error = "Les informations pour se connecter sont incorrectes."
