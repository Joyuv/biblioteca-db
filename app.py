from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,redirect,url_for,render_template,request
from flask_login import logout_user, login_user, current_user, login_required, LoginManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = "CHAVE SUPER SECRETA"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, nome):
        self.id = id
        # self.nome = nome
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(id):
    # GIVA: função que pega os dados do usuário a partir do id (de preferência retornar em um dicionário com os dados pra facilitar minha vida)
    
    return User(id)
    # return User(id, usuario['nome'])


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')


        # GIVA: função que checa se o email está presente na tabela usuários
        # if usuario não existe:
 
        senha_hash = generate_password_hash(senha)

        # GIVA: função que adiciona o usuário no banco com os seguintes dados
        #     Nome_usuario VARCHAR(255) NOT NULL, # é parametro da função
        #     Email VARCHAR(255), # é parametro da função
        #     Numero_telefone VARCHAR(15), # é parâmetro da função
        #     Senha_hash VARCHAR(255), # ESSE CAMPO NÃO ESTÁ PRESENTE NA TABELA QUE HUGO MANDOU, ADICIONA LÁ # é parâmetro da função
        #     Data_inscricao DATE, # DATA ATUAL
        #     Multa_atual DECIMAL(10, 2) # NO MOMENTO É 0
        
        # if usuario existe: (else)
        # exibe mensagem de erro
        # redireciona para cadastro de novo

        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # if usuario existe:
        
        # GIVA: função que pega os dados do usuário a partir do email (de preferência retornar em um dicionário com os dados pra facilitar minha vida)
        # if check_password_hash(usuario['Senha_hash'], senha)
        # login_user(usuario['ID_usuario'])

        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)