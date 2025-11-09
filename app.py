from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import (
    logout_user,
    login_user,
    current_user,
    login_required,
    LoginManager,
    UserMixin,
)
from database.db import *

initDB()

app = Flask(__name__)
app.config["SECRET_KEY"] = "CHAVE SUPER SECRETA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        # self.nome = nome

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(id):
    user = getUserById(id)
    return User(id, user["nome_usuario"])


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/livros")
def livros():
    livros = getBooks()
    nao_exibir = []
    if current_user.is_authenticated:
        livros_usuario = getUserBooks(current_user.id)
        
        for livro in livros_usuario:
            if livro["status_emprestimo"] != "devolvido":
                nao_exibir.append(livro["id_livro"])


    return render_template('livros/list.html', livros=livros, nao_exibir=nao_exibir)

@app.route('/livros/<livro_id>/emprestimo')
@login_required
def pegar_livro(livro_id):
    addUserBook(current_user.id, livro_id)
    return redirect(url_for("livros"))

@app.route('/livros/<emprestimo_id>/devolver')
@login_required
def devolver_livro(emprestimo_id):
    returnBook(emprestimo_id)

    return redirect(url_for("meus_emprestimos"))

@app.route('/meus-emprestimos')
@login_required
def meus_emprestimos():
    emprestimos = getUserBooks(current_user.id)

    return render_template('usuario/meus_emprestimos.html', emprestimos=emprestimos)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        senha = request.form.get("senha")

        user = getUserByEmail(email)

        if not user:
            senha_hash = generate_password_hash(senha)
            addUser(nome, email, telefone, senha_hash)
            return redirect(url_for("login"))
        else:
            flash("Este email já está cadastrado", "error")
            return redirect(url_for("cadastro"))
    return render_template("auth/cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        user = getUserByEmail(email)

        if user is not None:
            if check_password_hash(user["senha_hash"], senha):
                login_user(User(user["id_usuario"], user["nome_usuario"]))
            return redirect(url_for("index"))
        flash("Email ou senha incorreta", "error")

    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
