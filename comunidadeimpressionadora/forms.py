from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from comunidadeimpressionadora import app
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        with app.app_context():
            usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Adicionando o campo de edição de foto
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    # Adicionando os campos de escolha dos cursos
    curso_excel = BooleanField('Excel Impressionador')
    curso_vaba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    #Criamos a função que irá verificar a existencia do e-mail
    def validate_email(self, email):
        #Verificar se o cara mudou de email
        if current_user.email != email.data:
            #Verificamos o banco se esse email já consta no banco
            with app.app_context():
                usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail, por favor cadastre outro')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')

