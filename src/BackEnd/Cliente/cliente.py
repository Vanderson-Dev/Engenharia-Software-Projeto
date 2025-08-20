from .ArmazenaClienteBD import get_db_connection

class Cliente:
    def __init__(self, cpf):
        self.cpf = cpf
        self.dados = self.buscar_cliente()

    def buscar_cliente(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE cpf = %s", (self.cpf,))
        cliente = cursor.fetchone()
        cursor.close()
        conn.close()
        return cliente

    def existe(self):
        return self.dados is not None