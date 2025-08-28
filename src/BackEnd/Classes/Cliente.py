# Arquivo: src/BackEnd/Cadastro/Cliente.py
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime
from BackEnd.config import DB_CONFIG

# Função de conexão para o seu banco de dados local
def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
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

                # Pega o id do cliente criado
                cliente_id = cursor.lastrowid

                # Criar conta vinculada ao cliente
                sql_conta = "INSERT INTO Conta (saldo, usuario_id) VALUES (0.00, %s)"
                cursor.execute(sql_conta, (cliente_id,))

            conn.commit()
            return True
        except pymysql.IntegrityError:
            # Erro de CPF ou E-mail duplicado
            return False
        finally:
            if conn:
                conn.close()
    
    def autenticarCliente(email, senha):
        """Verifica se um cliente existe com o email e senha fornecidos."""
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM clientes WHERE email=%s AND senha=%s",
                    (email, senha)
                )
                cliente = cursor.fetchone()
            return cliente  # Retorna o dict do cliente ou None
        finally:
            if conn:
                conn.close()

    