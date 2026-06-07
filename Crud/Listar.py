from Database import conexao as db
from mysql.connector import Error
import time

def verificarConsulta(consulta_sql):
# Função para verificar consultar

    conexao_sql = db.conectar()
    if conexao_sql is None:
        print("Não foi possível estabelecer conexão com o banco.")
        return None
    
    cursor = None
    try:
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        return resultado
    
    except Error as e:
        print(f"Erro ao executar consulta: {e}")
        return None    
    
    finally:
        db.desconectar(conexao_sql, cursor)

def executar_consulta_com_parametros(consulta_sql, valores):
    # função para executar uma consulta SQL com parâmetros e retorna os resultados.

    conexao_sql = db.conectar()
    if conexao_sql is None:
        print("Erro de conexão com o banco.")
        return None
    cursor = None
    try:
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql, valores)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro na consulta: {e}")
        return None
    finally:
        db.desconectar(conexao_sql, cursor)



def listarTudo():
    # Função para exibir todos os produtos com paginação (5 por página)

    pagina = 1
    itens_por_pagina = 5

    while True:
        offset = (pagina - 1) * itens_por_pagina
        consulta_sql = """
            SELECT * FROM produtos
            ORDER BY id_produto
            LIMIT %s OFFSET %s
        """
        resultado = executar_consulta_com_parametros(consulta_sql, (itens_por_pagina, offset))

        if not resultado:
            if pagina == 1:
                print("\nNenhum produto encontrado.")
            else:
                print("\nFim da lista.")
            break

        print(f"\n--- Página {pagina} ---")
        for linha in resultado:
            print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")

        # Opções de navegação
        print(f"\n----- Página {pagina} -----")
        print("\n[1] Próxima página")
        if pagina > 1:
            print("[2] página anterior")
        print("[3] Sair da listagem")

        try:
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    pagina += 1
                
                case 2 if pagina > 1:
                    pagina -= 1

                case 3:
                    break

                case _:
                    print("\nERRO: a opção precisa ser um numero entre (1 ~ 3)")
        
        except ValueError:
            print("Entrada inválida. Digite um número inteiro válido.")


def listarNome(resultado):
    if not resultado:
        print("\nNenhum dado foi encontrado no sistema")
    else:
        for pos, linha in enumerate(resultado, start=1):
            print(f"\n{pos}º {linha[0]}")

def listarPreco(resultado):
    if not resultado:
        print("\nNenhum dado foi encontrado no sistema")
    else:
        for pos, linha in enumerate(resultado, start=1):
            print(f"\n{pos}º R${linha[0]:.2f}")

def listarEstoque(resultado):
    if not resultado:
        print("\nNenhum dado foi encontrado no sistema")
    else:
        for pos, linha in enumerate(resultado, start=1):
            print(f"\n{pos}º {linha[0]}")



def listarProdutos():
    # Função para Listar produtos
    
    print("=-"*10 + " LISTAR PRODUTOS " + "=-"*10)        
    while True:
        try:
            print(
            "\n[1] Listar nomes" 
            "\n[2] Listar Precos" 
            "\n[3] Listar estoques" 
            "\n[4] Listar todos os dados" 
            "\n[5] Voltar para o menu principal" 
        )
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    consulta_sql = "SELECT nome FROM produtos;"
                    resultado = verificarConsulta(consulta_sql)
                    listarNome(resultado)
                case 2:
                    consulta_sql = "SELECT preco FROM produtos;"
                    resultado = verificarConsulta(consulta_sql)
                    listarPreco(resultado)
                case 3:
                    consulta_sql = "SELECT estoque FROM produtos;"
                    resultado = verificarConsulta(consulta_sql)
                    listarEstoque(resultado)
                case 4:
                    consulta_sql = "SELECT * FROM produtos;"
                    resultado = verificarConsulta(consulta_sql)
                    listarTudo() 
                case 5:
                    print("\nRetornando.....")
                    time.sleep(1.5)
                    return
                case _:
                    print("\nOpção inválida. Tente novamente!")
        except ValueError:
            print("Entrada inválida. tente novamente!")

        