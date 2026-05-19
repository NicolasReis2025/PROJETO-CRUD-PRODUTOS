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


def listarTudo(resultado):
    if not resultado:
        print("\nNenhum produto foi encontrado no banco de dados")
    else:
        for linha in resultado:
            print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")


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
                    listarTudo(resultado) 
                case 5:
                    print("\nRetornando para o menu inicial.....")
                    time.sleep(1.5)
                    return
                case _:
                    print("\nOpção inválida. Tente novamente!")
        except ValueError:
            print("Entrada inválida. tente novamente!")

        