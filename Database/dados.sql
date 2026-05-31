-- 1. Criação do banco de dados (se não existir)
CREATE DATABASE IF NOT EXISTS crud_python;
USE crud_python;

-- 2. Tabela de PRODUTOS (já existente)
CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT NOT NULL,
    PRIMARY KEY (id_produto)
);

-- 3. Tabela de USUÁRIOS (para controle de quem fez cada ação)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    login VARCHAR(30) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('admin', 'operador') DEFAULT 'operador',
    PRIMARY KEY (id_usuario)
);

-- 4. Tabela de LOGS (auditoria)
CREATE TABLE IF NOT EXISTS logs_operacoes (
    id_log INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    operacao VARCHAR(20) NOT NULL,           -- INSERT, UPDATE, DELETE, ACESSO
    tabela_afetada VARCHAR(50) NOT NULL,
    id_registro INT,                          -- ID do registro alterado (ex: id_produto)
    detalhes TEXT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_log),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
);

-- 5. Dados iniciais (população mínima para teste)


INSERT INTO usuarios (nome, login, senha_hash, perfil) VALUES
('Administrador', 'admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin');

-- Opcional: inserir um operador comum (senha = operador123)
INSERT INTO usuarios (nome, login, senha_hash, perfil) VALUES
('Operador Padrão', 'operador', '$2b$12$K9LmNpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjK', 'operador');

-- Inserir produtos de exemplo (seus dados originais)
INSERT INTO produtos (nome, preco, estoque) VALUES
('Notebook', 3500.00, 10),
('Mouse', 89.90, 50),
('Teclado', 149.90, 30),
('Monitor', 1200.00, 15),
('Headset', 250.00, 25);