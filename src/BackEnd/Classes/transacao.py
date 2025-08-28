from Conta import Conta

class Transacao:
    def __init__(self, cpf_origem, cpf_destino, valor):
        self.conta_origem = Conta(cpf_origem)
        self.conta_destino = Conta(cpf_destino)
        self.valor = valor

    def validar_saldo(self):
        saldo = self.conta_origem.consultar_saldo()
        return saldo is not None and saldo >= self.valor

    def realizar(self):
        if not self.validar_saldo():
            return False, "Saldo insuficiente"
        self.conta_origem.debitar(self.valor)
        self.conta_destino.creditar(self.valor)
        return True, "Transferência realizada com sucesso"