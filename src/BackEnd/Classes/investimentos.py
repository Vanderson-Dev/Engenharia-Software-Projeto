import random

class Investimento:
    def __init__(self, valor):
        self.valor = valor

    def investir(self, tipo):
        resultado = {
            'valor_investido': self.valor,
            'valor_final': 0,
            'ganhou': False,
            'descricao': ''
        }

        if tipo == 'seguro':  # Investimento 1
            chance = 0.25
            aumento = 0.15
            if random.random() < chance:
                resultado['valor_final'] = round(self.valor * (1 + aumento), 2)
                resultado['ganhou'] = True
                resultado['descricao'] = 'Você ganhou 15% sobre o valor investido!'
            else:
                resultado['valor_final'] = self.valor
                resultado['descricao'] = 'Não houve ganho, valor mantido.'
        elif tipo == 'arriscado':  # Investimento 2
            chance = 0.20
            aumento = 0.70
            if random.random() < chance:
                resultado['valor_final'] = round(self.valor * (1 + aumento), 2)
                resultado['ganhou'] = True
                resultado['descricao'] = 'Você ganhou 70% sobre o valor investido!'
            else:
                resultado['valor_final'] = 0
                resultado['descricao'] = 'Você perdeu todo o valor investido.'
        elif tipo == 'simulacao':  # Investimento 3
            chance = 0.05
            aumento = 1.00
            if random.random() < chance:
                resultado['valor_final'] = round(self.valor * (1 + aumento), 2)
                resultado['ganhou'] = True
                resultado['descricao'] = 'Você ganhou 100% sobre o valor investido!'
            else:
                resultado['valor_final'] = 0
                resultado['descricao'] = 'Você perdeu todo o valor investido.'
        elif tipo == 'teste':
            chance = 0.80
            aumento = 0.50
            if random.random() < chance:
                resultado['valor_final'] = round(self.valor * (1 + aumento), 2)
                resultado['ganhou'] = True
                resultado['descricao'] = 'Você ganhou 50% sobre o valor investido!'
            else:
                resultado['valor_final'] = self.valor
                resultado['descricao'] = 'Não houve ganho, valor mantido.'
        else:
            resultado['descricao'] = 'Tipo de investimento inválido.'

        return resultado

def realizar_investimento(conn, usuario_id, valor, tipo):
    """
    Atualiza o saldo do usuário após o investimento.
    """
    investimento = Investimento(valor)
    resultado = investimento.investir(tipo)

    cursor = conn.cursor()
    # Busca saldo atual
    cursor.execute("SELECT saldo FROM Conta WHERE usuario_id = %s", (usuario_id,))
    conta = cursor.fetchone()
    if not conta or conta['saldo'] < valor:
        cursor.close()
        return {'erro': 'Saldo insuficiente.'}

    # Remove valor investido
    novo_saldo = conta['saldo'] - valor

    # Adiciona valor final do investimento (se ganhou algo)
    novo_saldo += resultado['valor_final']

    # Atualiza saldo no banco
    cursor.execute("UPDATE Conta SET saldo = %s WHERE usuario_id = %s", (novo_saldo, usuario_id))
    conn.commit()
    cursor.close()

    resultado['novo_saldo'] = round(novo_saldo, 2)
    return resultado