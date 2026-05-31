from Database import conexao as db
from mysql.connector import Error
import time


def verificarConsulta(consulta_sql, valores):
    # Função para verificar consulta


    conexao_sql = db.conectar()
    if conexao_sql is None:
        print("Não foi possível estabelecer conexão com o banco.")
        return None

    cursor = None
    try:
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql, valores)
        resultado = cursor.fetchall()
        return resultado
    
    except Error as e:
        print(f"Erro ao executar consulta: {e}")
        return None
    
    finally:
        db.desconectar(conexao_sql, cursor)
        

def exibirProdutos(resultado):
    # Função para exibir produtos

    if resultado:
        for linha in resultado:
            print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")
    else:
        print("\nNenhum produto foi encontrado no banco de dados")


def buscarProduto():
    # Função para buscar produto

    print("=-"*10 + " BUSCAR PRODUTO " + "=-"*10)
    while True:
        try:
            print(
            "\n[1] Buscar por id" 
            "\n[2] Buscar por nome"  
            "\n[3] Voltar para o menu Principal")
            
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    id = int(input("Digite o id do produto para busca-lo: "))
                    consulta_sql = "SELECT * FROM produtos WHERE id_produto = %s;"
                    valores = (id, )
                    resultado = verificarConsulta(consulta_sql, valores)
                    exibirProdutos(resultado)

                case 2:
                    nome = str(input("Digite o nome do produto para busca-lo: ")).strip()
                    consulta_sql = "SELECT * FROM produtos WHERE nome LIKE %s;"
                    valores = (f"%{nome}%", )
                    resultado = verificarConsulta(consulta_sql, valores)
                    exibirProdutos(resultado)

                case 3:
                    print("\nRetornando.....")
                    time.sleep(1.5)
                    return
                
                case _:
                    print("\nERRO: opção inválida. Tente novamente!")
        
        except ValueError:
            print("Entrada inválida. Tente novamente!")
        
    



                    




