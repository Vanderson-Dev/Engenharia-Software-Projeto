from .ArmazenaClienteBD import get_db_connection

class Conta:
    def __init__(self, cpf):
        self.cpf = cpf

    def consultar_saldo(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT saldo FROM clientes WHERE cpf = %s", (self.cpf,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado['saldo'] if resultado else None

    def debitar(self, valor):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET saldo = saldo - %s WHERE cpf = %s", (valor, self.cpf))
        conn.commit()
        cursor.close()
        conn.close()

    def creditar(self, valor):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET saldo = saldo + %s WHERE cpf = %s", (valor, self.cpf))
        conn.commit()
        cursor.close()
        conn.close()