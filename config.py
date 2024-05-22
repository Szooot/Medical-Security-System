from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "admin"

# Konfiguracja bazy danych PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123qweasd@localhost/hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)