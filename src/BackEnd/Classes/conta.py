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
        self.id = id              # ID do cliente
        self.cpf = cpf            # CPF do cliente
        self.saldo = saldo        # Saldo atual da conta

    def verExtrato(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT saldo FROM Conta WHERE usuario_id = %s", (self.id,))
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
        cursor.execute("UPDATE Conta SET saldo = saldo - %s WHERE usuario_id = %s", (valor, self.id))
        cursor.execute(
            """
            INSERT INTO transactions (account_id, type, amount, description)
            VALUES (%s, 'saque', %s, %s)
            """,
            (self.id, valor, 'Saque realizado')
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def depositar(self, valor):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Conta SET saldo = saldo + %s WHERE usuario_id = %s", (valor, self.id))
        cursor.execute(
            """
            INSERT INTO transactions (account_id, type, amount, description)
            VALUES (%s, 'deposito', %s, %s)
            """,
            (self.id, valor, 'Depósito realizado')
        )
        conn.commit()
        cursor.close()
        conn.close()

    def transferir(self, valor, conta_destino):
        saldo_atual = self.verExtrato()
        if saldo_atual is None or saldo_atual < valor:
            return False
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Conta SET saldo = saldo - %s WHERE usuario_id = %s", (valor, self.id))
            cursor.execute("UPDATE Conta SET saldo = saldo + %s WHERE usuario_id = %s", (valor, conta_destino.id))
            cursor.execute(
            """
            INSERT INTO transactions (account_id, type, amount, target_account_id, description)
            VALUES (%s, 'transferencia', %s, %s, %s)
            """,
            (self.id, valor, conta_destino.id, f'Transferência para usuário {conta_destino.id}')
        )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
