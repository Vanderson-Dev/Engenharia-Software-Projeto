# Plataforma Web para Internet Banking
![Badge opcional](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

## Objetivo do Sistema

Este projeto tem como objetivo o desenvolvimento de um sistema de Internet Banking que permita aos usuários realizarem operações bancárias de forma digital e acessível. A plataforma será desenvolvida com foco na experiência do usuário e funcionalidades, oferecendo um ambiente confiável para o gerenciamento de contas pessoais.

O sistema permitirá que os usuários acessem suas contas por meio de login, visualizem informações como saldo, dados pessoais, histórico de transações, empréstimos, além de possibilitar a realização de investimentos em produtos financeiros, além de possibilitar a atualização de seus dados cadastrais.

## Membros da equipe e papel

- Arthur Pinheiro [Back-End]
- Davi Torres [Back-End/Banco de Dados]
- Vanderson Guimarães [Full-Stack]
- Weder [Back-End]
- William Andrade [Full-Stack]

## Tecnologias Utilizadas

- HTML/CSS
- Python
- MySQL

## Backlog do Produto

- [ ] Como usuário, quero poder fazer login para acessar minha conta com segurança.
- [ ] Como usuário, quero fazer transferências bancárias para movimentar meu dinheiro entre contas.
- [ ] Como usuário, quero aumentar o limite do cartão.
- [ ] Como usuário, quero investir meu dinheiro em produtos financeiros (como CDB, LCI) para obter rentabilidade.
- [ ] Como usuário, quero depositar dinheiro na minha conta para aumentar meu saldo e poder usá-lo para futuras transações.
- [ ] Como usuário, quero solicitar um empréstimo para obter crédito e financiar meus projetos pessoais.
- [ ] Como usuário, quero visualizar um extrato detalhado com todas as minhas transações.
- [ ] Como usuário, quero criar uma nova conta, inserindo minhas informações pessoais.
- [ ] Como usuário, quero visualizar os valores das ações, acompanhados de indicadores que mostrem se elas tiveram queda ou aumento.

## Backlog da Sprint

- ### História 1: Como usuário, quero poder fazer login para acessar minha conta com segurança.

Tarefas e responsáveis:

- Desenvolver autenticação de usuário (e-mail/senha) [Vanderson Guimarães]

- Implementar proteção contra acessos não autorizados [Vanderson Guimarães]

- Criar tela de login com HTML/CSS [William Andrade]

- ### História 2: Como usuário, quero fazer transferências bancárias para movimentar meu dinheiro entre contas.

Tarefas e responsáveis:

- Criar lógica para transferência entre contas [Arthur Pinheiro]

- Validar saldo disponível antes da operação [Arthur Pinheiro]

- Registrar histórico de transações [Weder]

- ### História 3: Como usuário, quero aumentar o limite do cartão.

Tarefas e responsáveis:

- Criar regras para aprovação de aumento de limite [Davi Torres]

- Implementar comunicação com banco de dados [Vanderson Guimarães]

- Exibir notificações ao usuário sobre aprovação ou recusa [William Andrade]

 - ### História 4: Investimentos financeiros (CDB, LCI)

Responsável: Davi Torres

Tarefas:

- Criar interface para escolha de investimento [Vanderson Guimarães]

- Implementar lógica de rendimento e resgate [William Andrade]

- Integrar com banco de dados para registro [Vanderson Guimarães]

### História 5: Depósito de dinheiro na conta

Responsável: Arthur Pinheiro

Tarefas:

- Implementar funcionalidade de depósito

- Validar transação e atualizar saldo do usuário

- Criar interface de confirmação de depósito

### História 6: Solicitação de empréstimo

Responsável: Vanderson Guimarães / William Andrade

Tarefas:

- Criar regras de aprovação para solicitação de crédito

- Desenvolver tela para cadastro de empréstimos

- Integrar sistema com cálculo de taxas e parcelas

### História 7: Criar uma Nova Conta

Responsável: Davi Torres / William Andrade

Tarefas:

- Definir requisitos e campos necessários para cadastro

- Criar interface para cadastro do usuário

- Implementar a estrutura do banco de dados para armazenar as informações do cliente

### História 8: Exibir extrato detalhado

Responsável: Vanderson Guimarães / Davi Torres

Tarefas:

- Criar a Interface de Exibição do Extrato.

- Integrar com o Sistema de Transações.

- Definir Critérios de Exibição.

### História 9: Visualizar Valores das Ações com indicadores de variação

Responsável:

Tarefas:

- Criar a interface de exibição das ações.

- Configurar API externa para mostrar a cotação das ações
