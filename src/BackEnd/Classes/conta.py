import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="admin",
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor
    )

class Conta:
    def __init__(self, cpf, saldo, id):
        self.id = id
        self.cpf = cpf
        self.saldo = saldo

    def verExtrato(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT saldo FROM clientes WHERE cpf = %s", (self.cpf,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado['saldo'] if resultado else None

    def sacar(self, valor):
        saldo_atual = self.verExtrato()
        if saldo_atual is None or saldo_atual < valor:
            return False
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET saldo = saldo - %s WHERE cpf = %s", (valor, self.cpf))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def depositar(self, valor):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET saldo = saldo + %s WHERE cpf = %s", (valor, self.cpf))
        conn.commit()
        cursor.close()
        conn.close()

    '''def transferir(self, valor, conta_destino):
        saldo_atual = self.verExtrato()
        if saldo_atual is None or saldo_atual < valor:
            return False
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE clientes SET saldo = saldo - %s WHERE cpf = %s", (valor, self.cpf))
            cursor.execute("UPDATE clientes SET saldo = saldo + %s WHERE cpf = %s", (valor, conta_destino.cpf))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()'''


