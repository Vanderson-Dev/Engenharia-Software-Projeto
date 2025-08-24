# Arquivo: src/BackEnd/Cadastro/Cliente.py
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime

# Função de conexão para o seu banco de dados local
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="Banco",
        cursorclass=DictCursor
    )

class Cliente:
    def __init__(self, nome, endereco, cpf, data_nascimento, sexo, email, senha):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.email = email
        self.senha = senha # Lembrete: senha em texto puro por enquanto

    def cadastrar(self):
        """Salva os dados do cliente no banco de dados."""
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO clientes
                    (nome, endereco, cpf, data_nascimento, sexo, email, senha, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    self.nome, self.endereco, self.cpf, self.data_nascimento,
                    self.sexo, self.email, self.senha, datetime.now()
                ))
            conn.commit()
            return True
        except pymysql.IntegrityError:
            # Erro de CPF ou E-mail duplicado
            return False
        finally:
            if conn:
                conn.close()