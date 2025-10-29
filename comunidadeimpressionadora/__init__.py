from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'cff0c6ed1f974f20c4fdbbe2aa03c1b8'
#Vai verificar se existe a variavel de ambiente se não existir vai usar o banco de teste
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:OpUyYkGrEflzOcrNqkveRorDMpNAzQeS@hopper.proxy.rlwy.net:24219/railway'


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, efetue o login ou se cadastre para visualizar a página'
login_manager.login_message_category = 'alert-info'




from comunidadeimpressionadora import routes
