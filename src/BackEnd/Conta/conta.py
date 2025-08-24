from ArmazenaClienteBD.ArmazenaClienteBD import get_db_connection

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
        # Verifica se o saldo é suficiente antes de debitar
        saldo_atual = self.consultar_saldo()
        if saldo_atual is None or saldo_atual < valor:
            return False  # Saldo insuficiente ou conta não encontrada
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

