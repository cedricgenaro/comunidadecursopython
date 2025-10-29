from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import inspect
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cff0c6ed1f974f20c4fdbbe2aa03c1b8'

# Detecta se está no Railway (Postgres) ou local (SQLite)
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, efetue o login ou se cadastre para visualizar a página'
login_manager.login_message_category = 'alert-info'

# 🔹 Cria as tabelas automaticamente se ainda não existirem
with app.app_context():
    inspector = inspect(database.engine)
    tabelas_existentes = inspector.get_table_names()
    if not tabelas_existentes:  # se o banco estiver vazio
        database.create_all()
        print("Banco inicializado e tabelas criadas com sucesso!")
    else:
        print("Banco já possui tabelas, nenhuma criação necessária.")

from comunidadeimpressionadora import routes


