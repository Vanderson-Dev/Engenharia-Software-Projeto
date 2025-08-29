DROP DATABASE IF EXISTS Banco;
CREATE DATABASE Banco;
USE Banco;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco TEXT NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    sexo VARCHAR(10) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE Conta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    saldo DOUBLE DEFAULT 0,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES clientes(id)
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,         -- ID da conta do cliente
    type ENUM('saque', 'deposito', 'transferencia') NOT NULL,
    amount DECIMAL(15,2) NOT NULL,  -- valor da movimentação
    target_account_id INT DEFAULT NULL, -- só usado em transferências
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255)
);
