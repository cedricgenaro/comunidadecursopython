from flask import render_template, redirect, url_for, request, flash, abort
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image



@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # exibir msg de login bem sucedido
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}.', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return  redirect(par_next)
            else:
                # redirecionar para a homepage
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #Preparando dados do formulário para inserir na tabela Usuário
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('Utf-8')
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()

        # Criou uma conta com sucesso
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}.', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito Com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():

    foto_perfil = url_for('static', filename=f'/fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()

        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criarpost.html', form=form )

def salvar_imagem(imagem):
    # criamos um código aleatório
    codigo = secrets.token_hex(8)
    # Aplicando o nome ao arquivo de imagem
        # Separamos o nome do arquivo em duas partes - nome e extensão
    nome, extensao = os.path.splitext(imagem.filename)
    # Criamos o nome combinado a extensão
    nome_arquivo = nome + codigo + extensao
    # Reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # Salvar a imagem na pasta fotos_perfil
        # Pegar o caminho completo da pasta foto_perfil
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil/', nome_arquivo)
        # Salvar o arquivo
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        #verificar se o nome do campo é de um checkbox e se está selecionado.
        if 'curso_' in campo.name and campo.data:
            #Adicionar o texto do campo .label  Ex(Excel Impressionador) na lista de cursos
            lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)



@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        # Se o formulario for submetido com sucesso
        user_logado = Usuario.query.filter_by(id=current_user.id).first()
        # Alteramos os dados do usuário atual
        user_logado.username = form.username.data
        user_logado.email = form.email.data
        # Verificar se o usuário carregou uma foto
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            # mudar o campo foto_perfil do usuário para o novo nome da imagem
            user_logado.foto_perfil = nome_imagem
        #Pegamnos os cursos selecionados pelo usuário
        user_logado.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil editado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        for campo in form:
            lista_cursos = current_user.cursos.split(';')
            if 'curso_' in campo.name:
                if campo.label.text in lista_cursos:
                    campo.data = True


    foto_perfil = url_for('static', filename=f'/fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if post.autor == current_user:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

