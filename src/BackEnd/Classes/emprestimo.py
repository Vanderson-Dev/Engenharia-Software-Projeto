from datetime import datetime

class Emprestimo:
    def __init__(self, valor, taxa_juros, parcelas, cliente_id, data_solicitacao=None, aprovado=False):
        self.valor = valor
        self.taxa_juros = taxa_juros
        self.parcelas = parcelas
        self.cliente_id = cliente_id
        self.data_solicitacao = data_solicitacao or datetime.now()
        self.aprovado = aprovado

    def calcular_valor_total(self):
        """Calcula o valor total a ser pago considerando juros simples."""
        return round(self.valor * (1 + self.taxa_juros * self.parcelas), 2)

    def aprovar(self):
        self.aprovado = True

    def rejeitar(self):
        self.aprovado = False

    def __repr__(self):
        status = "Aprovado" if self.aprovado else "Pendente"
        return (f"<Emprestimo cliente={self.cliente_id} valor={self.valor} "
                f"juros={self.taxa_juros} parcelas={self.parcelas} status={status}>")