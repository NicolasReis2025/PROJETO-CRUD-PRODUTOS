from Database import conexao as db
from mysql.connector import Error
import time

def deletarProduto():
    # Função para deletar produto

    print("=-"*10 + " DELETAR PRODUTO " + "=-"*10)
    while True:
        try:
            id = int(input("\nDigite o id do produto para removê-lo: "))
            break
        
        except ValueError:
            print("\nERRO: entrada inválida. Tente novamente!")
            continue
    
    try:
            conexao_sql = db.conectar()
            cursor = conexao_sql.cursor()

            consulta_sql = "SELECT * FROM produtos WHERE id_produto = %s"
            cursor.execute(consulta_sql, (id, ))
            resultado = cursor.fetchall()
            
            if not resultado:
                    print("\nNenhum produto cadastrado com esse id no banco de dados")
                    return
            
            for linha in resultado:
                print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")


            while True:
                    try:
                        print("\nDeseja realmente deletar esse produto? ")
                        print("\n[1] Sim\n[2] Não")
                        confirmacao = int(input("Digite uma opção: "))
                        match confirmacao:
                            case 1:
                                remover_sql = "DELETE FROM produtos WHERE id_produto = %s"
                                cursor.execute(remover_sql,(id,))
                                conexao_sql.commit()
                                print("\nProduto removido com sucesso")
                                return
                            case 2:
                                print("\nRetornando para o menu Principal.....")
                                time.sleep(1.5)
                                return
                            case _:
                                print("ERRO: opção inválida. Digite 1 para SIM ou 2 para NÃO.")
                    
                    except ValueError:
                        print("\nEntrada inválida. Tente novamente!")
    except Error as e:
        print(f"\nErro ao conectar no banco de dados: {e}")

    finally:
        db.desconectar(conexao_sql, cursor)
                         
                         
                        

    
            

