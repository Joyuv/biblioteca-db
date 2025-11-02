import mysql.connector
from datetime import datetime


def addUser(nome, email, numero, senha_hash):

    con = mysql.connector.connect(
        user="root", password="", host="127.0.0.1", database="db_trabalho3B"
    )
    cur = con.cursor()

    adduser = (
        "INSERT INTO Usuarios"
        "(Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    date = datetime.today().strftime("%Y-%m-%d")

    usuario = (nome, email, numero, senha_hash, date, 0)

    cur.execute(adduser, usuario)

    con.commit()
    cur.close()
    con.close()


def getUserById(id):
    con = mysql.connector.connect(
        user="root", password="", host="127.0.0.1", database="db_trabalho3B"
    )
    cur = con.cursor(dictionary=True)

    query = (
        "SELECT Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual"
        "WHERE ID_usuario = %s"
    )

    cur.execute(query, (id))
    data = cur.fetchone()

    user = {
        "Nome_usuario": data["Nome_usuario"],
        "Email": data["Email"],
        "Numero_telefone": data["Numero_telefone"],
        "Senha_hash": data["Senha_hash"],
        "Data_inscricao": data["Data_inscricao"],
        "Multa_atual": data["Multa_atual"],
    }
    cur.close()
    con.close()
    return user


def getUserByEmail(email):
    con = mysql.connector.connect(
        user="root", password="", host="127.0.0.1", database="db_trabalho3B"
    )
    cur = con.cursor(dictionary=True)

    query = (
        "SELECT Nome_usuario, Email, Numero_telefone, Senha_hash, Data_inscricao, Multa_atual"
        "WHERE Email = %s"
    )

    cur.execute(query, (email))
    data = cur.fetchone()

    user = {
        "Nome_usuario": data["Nome_usuario"],
        "Email": data["Email"],
        "Numero_telefone": data["Numero_telefone"],
        "Senha_hash": data["Senha_hash"],
        "Data_inscricao": data["Data_inscricao"],
        "Multa_atual": data["Multa_atual"],
    }
    cur.close()
    con.close()
    return user
