# CRUD de Produtos - Python + MySQL

Sistema de gerenciamento de produtos (CRUD completo) desenvolvido em Python com banco de dados MySQL. Ideal para aprender conceitos de conexão com banco, consultas parametrizadas, modularização e tratamento de erros.

## Funcionalidades

- **Adicionar** produto (com validação de nome duplicado, preço e estoque)
- **Atualizar** produto (com dupla confirmação e exibição dos dados atuais)
- **Buscar** produto (por ID ou por parte do nome)
- **Deletar** produto (com confirmação e exibição do produto)
- **Listar** produtos (nomes, preços, estoques ou todos os dados)
- **Relatórios**:
  - Valor total do estoque (por produto)
  - Produto mais caro / mais barato
  - Produto com maior / menor estoque
  - Média de itens no estoque

## Tecnologias utilizadas

- Python 3.10+
- MySQL (ou MariaDB)
- Bibliotecas:
  - `mysql-connector-python` – conexão com o banco
  - `python-dotenv` – gerenciamento de variáveis de ambiente

## Como executar o projeto passo a passo

### Pré‑requisitos

- Python 3.10 ou superior instalado
- MySQL Server instalado e em execução
- (Opcional) Git para clonar o repositório

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/NicolasReis2025/PROJETO-CRUD-PRODUTOS.git
cd PROJETO-CRUD-PRODUTOS

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

### 3. Instale as dependências
```bash
pip install -r requirements.txt

### 4. Configure o banco de dados

### 5. Configure as variáveis de ambiente

### 6. Execute o programa
```bash
python main.py


### Estrutura do projeto
```bash

PROJETO-CRUD-PRODUTOS/
├── Crud/                     # Operações CRUD
│   ├── Adicionar.py
│   ├── Atualizar.py
│   ├── Buscar.py
│   ├── Deletar.py
│   └── Listar.py
├── Database/                 # Conexão com o banco
│   ├── conexao.py
│   └── dados.sql
├── Relatorio/                # Relatórios analíticos
│   └── DadosAnalisticos.py
├── menus.py                  # Menu principal
├── main.py                   # Ponto de entrada
├── requirements.txt          # Dependências
├── .env                      # Credenciais (não versionado)
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Este arquivo


### Autor
```bash
Nicolas Reis – GitHub – nicolas.reis2024@gmail.com