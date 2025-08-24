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
    def __init__(self, cpf):
        self.cpf = cpf

    def consultar_saldo(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT saldo FROM clientes WHERE cpf = %s", (self.cpf,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado['saldo'] if resultado else None

    def debitar(self, valor):
        saldo_atual = self.consultar_saldo()
        if saldo_atual is None or saldo_atual < valor:
            return False
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET saldo = saldo - %s WHERE cpf = %s", (valor, self.cpf))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def creditar(self, valor):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET saldo = saldo + %s WHERE cpf = %s", (valor, self.cpf))
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    conta = Conta("12345678900")
    print("Saldo atual:", conta.consultar_saldo())

    if conta.debitar(100):
        print("Débito realizado com sucesso!")
    else:
        print("Saldo insuficiente ou cliente não encontrado.")

    conta.creditar(400)
    print("Saldo após crédito:", conta.consultar_saldo())
