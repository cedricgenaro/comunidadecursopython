from comunidadeimpressionadora import database, login_manager, app
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    cursos = database.Column(database.String, nullable=False, default='Não Informado')
    posts = database.relationship('Post', backref='autor', lazy=True)

    def contar_cursos(self):
        lista_cursos = self.cursos.split(';')
        return len(lista_cursos)

    def contar_posts(self):
        return len(self.posts)

# @login_manager.user_loader
# def load_user(user_id):
#     return Usuario.query.get(int(user_id))



class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'),  nullable=False)

