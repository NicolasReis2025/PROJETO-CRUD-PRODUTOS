import csv
import os
import time
from datetime import datetime
from Database import conexao as db
from mysql.connector import Error
from Auditoria import logs

PASTA_CSV = os.path.join(os.path.dirname(__file__), 'CSV')

def garantir_pasta():
    # Função para criar a pasta CSV se ela não existir."""
    if not os.path.exists(PASTA_CSV):
        os.makedirs(PASTA_CSV)
        print(f"Pasta criada: {PASTA_CSV}")


def nome_arquivo(base):
    # Função para gerar um nome único para o arquivo CSV com timestamp.

    garantir_pasta() 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome = f"{base}_{timestamp}.csv"
    return os.path.join(PASTA_CSV, nome)


def exportar_produtos():
    # Função para exportar todos os produtos para CSV.

    print("\n--- Exportando produtos...")
    time.sleep(1.5)
    conexao = db.conectar()
    if not conexao:
        print("Erro de conexão com o banco.")
        return

    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM produtos ORDER BY id_produto")
        dados = cursor.fetchall()

        if not dados:
            print("Nenhum produto encontrado.")
            return

        arquivo = nome_arquivo("produtos_completo")
        with open(arquivo, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["ID", "Nome", "Preço (R$)", "Estoque"])
            writer.writerows(dados)  
        print(f"Produtos exportados com sucesso!\nArquivo: {arquivo}")

    except Error as e:
        print(f"❌ Erro ao consultar banco: {e}")
    finally:
        db.desconectar(conexao, cursor)


def exportar_estoque_baixo():
    print("\nExportando produtos....")
    time.sleep(1.5)

    conexao = db.conectar()
    if not conexao:
        print("\nErro de conexão com o banco")
        return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM produtos where estoque <= 5 ORDER BY estoque;")
        dados = cursor.fetchall()

        if not dados:
            print("Não há produtos com estoque baixo")
            return 
        
        arquivo = nome_arquivo("Produtos_estoque_baixo")
        with open(arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ID", "Nome", "Preço (R$)", "Estoque"])
            writer.writerows(dados)       

        print(f"Produtos com estoque baixo exportados!\nArquivo: {arquivo}")

    except Error as e:
        print(f"❌ Erro: {e}")

    finally:
        db.desconectar(conexao, cursor)     


def exportar_valor_total_estoque():
    print("\nExportando produtos....")
    time.sleep(1.5)

    conexao = db.conectar()
    if not conexao:
        print("\nErro de conexão com o banco")
        return

    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_produto, nome_produto, preco * estoque as valor_total FROM produtos ORDER BY valor_total DESC;")
        dados = cursor.fetchall()

        if not dados:
            print("Não há produtos cadastrados no banco de dados")
        
        arquivo = nome_arquivo("Valor_estoque_por_produto")
        with open(arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Produto", "Valor Total (R$)"])
            writer.writerows(dados)

            print(f"Valor total exportado!\nArquivo: {arquivo}")

    except Error as e:
        print(f"Erro: {e}")

    finally:
        db.desconectar(conexao, cursor)

def exportar_logs():
    # Funçaõ para expotar logs

    logs = logs.buscar_todos_logs(limite=100)
    if not logs:
        print("Nenhum log encontrado.")
        return

    arquivo = nome_arquivo("logs_ultimos_100")
    with open(arquivo, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Data/Hora", "Usuário", "Operação", "Tabela", "ID Registro", "Detalhes"])
        for log in logs:
            data_str = log[0].strftime("%Y-%m-%d %H:%M:%S") if log[0] else ""
            writer.writerow([data_str, log[1], log[2], log[3], log[4], log[5]])

    print(f"Logs exportados com sucesso!\nArquivo: {arquivo}")


def menuCsv():
    print("=-=-= Exportar csv =-=-=\n")
    print("[1] Exportar produtos")
    print("[2] Exportar produtos com estoque baixo (≤5)")
    print("[3] Valor total do estoque por produto")
    print("[4] Logs completos (últimos 100)")
    print("[5] voltar para o menu inicial")
    
    while True:
        try:
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    exportar_produtos()
                case 2:
                    exportar_estoque_baixo()
                case 3:
                    exportar_valor_total_estoque()
                case 4:
                    exportar_logs()
                case 5:
                    print("\nRetornando...")
                    time.sleep(1.5)
                    return
                case _:
                    print("\nOpção inválida: digite um numero entre (1 - 5)")

        except ValueError:
            print("\nERRO: a opção precisa ser um numero inteiro válido")

