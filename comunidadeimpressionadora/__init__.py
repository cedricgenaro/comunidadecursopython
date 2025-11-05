from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy


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

# Para criar as tabelas é preciso importar o arquivo models
from comunidadeimpressionadora import models

# A engine vai avaliar o nosso banco de dados
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# Agora temos que verificar se a tabela de usuários está criada (tabela principal e o nome sempre em minusculo)
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table('usuario'):
    with app.app_context():
        # Por segurança devemos apagar as tabelas que já existem depois que fizemos o deploy
        database.drop_all()
        # Caso não tenha a tabela usuario, então irá criar todas as tabelas
        database.create_all()
        print('Base de dados criado')
else:
    print('Base de Dados criado')



from comunidadeimpressionadora import routes
