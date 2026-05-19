
---- CRIAR TABELA -----

create table if not exists produtos(
    id_produto int not null auto_increment,
    nome varchar(50) not null,
    preco decimal(10, 2) not null,
    estoque int not null,
    primary key(id_produto)
);


---- Adicionar valores iniciais na tabela ----


INSERT INTO produtos (nome, preco, estoque) VALUES
('Notebook',  3500.00, 10),
('Mouse',       89.90, 50),



