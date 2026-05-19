from  Database import conexao as db
from mysql.connector import Error
import time

def menuRelatorio():
# Função para mostrar o menu do relatório
    print("-="*10 + " MENU DE RELATÓRIO " + "-="*10)
    while True:
        try:
            print(
            "\n[1] Valor total de estoque (R$)" 
            "\n[2] Produto com maior preço" 
            "\n[3] Produto com menor preço" 
            "\n[4] Produto com maior quantidade em estoque" 
            "\n[5] Produto com menor quantidade em estoque"
            "\n[6] Quantidade média de itens em estoque (unidades)" 
            "\n[7] Voltar para o menu principal")
            
            opcao = int(input("Digite uma opção: "))
            match opcao:
                case 1:
                    valorEstoque()
                case 2:
                    produtoMaiorPreco()
                case 3:
                    produtoMenorPreco()
                case 4:
                    produtoMaiorEstoque()
                case 5:
                    produtoMenorEstoque()
                case 6:
                    mediaEstoque()
                case 7:
                    print("\nVoltando para o menu Principal.....")
                    time.sleep(1.5)
                    return
                case _:
                    print("ERRO: opção inválida. Tente novamente!")
                    continue
        except ValueError:
            print("Entrada inválida. Digite uma opção válida entre (1 a 7)")
    


def valorEstoque():
# Função para mostrar Valor total de estoque por produto

    print("\n" + "-="*10 + " RELATÓRIO DO VALOR TOTAL POR PRODUTO " + "-="*10)
    try:
        consulta_sql = """ SELECT nome as nome_produto, preco * estoque as valor_estoque FROM produtos;"""
        conexao_sql = db.conectar()
        cursor = conexao_sql.cursor()

        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                print(f"\nNome: {linha[0]} | valor de estoque: R${linha[1]:.2f}")
        else:
            print("\nNenhum produto foi cadastrado no banco de dados")
    
    except Error as e:
        print(f"\nErro ao conectar ao banco de dados: {e}")
    
    finally:
        db.desconectar(conexao_sql, cursor)

def produtoMaiorPreco():
# Função para mostrar produto com menor preço(R$)

    print("\n" + "-="*10 + " PRODUTO COM MAIOR PREÇO (R$) " + "-="*10)

    try:
        consulta_sql = """
        SELECT * FROM  produtos
        ORDER BY preco DESC LIMIT 1;"""

        conexao_sql = db.conectar()
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")
        else:
            print("\nNenhum produto foi encontrado no banco de dados")

    except Error as e:
        print(f"\nErro ao conectar ao banco de dados: {e}")
    
    finally:
        db.desconectar(conexao_sql, cursor)

def produtoMenorPreco():
# Função para mostrar produto com menor preço (R$)

    print("\n" + " -="*10 + " PRODUTO COM MENOR PREÇO (R$) " + "-="*10)

    try:
        consulta_sql = """
        SELECT * FROM  produtos
        ORDER BY preco ASC LIMIT 1;"""

        conexao_sql = db.conectar()
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql)

        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")
        else:
            print("\nNenhum produto foi encontrado no banco de dados")

    except Error as e:
        print(f"\nErro ao conectar ao banco de dados: {e}")
    
    finally:
        db.desconectar(conexao_sql, cursor)

def produtoMenorEstoque():
# Função para mostrar produto com menor estoque

        print("\n" + " -="*10 + " PRODUTO COM MENOR ESTOQUE " + "-="*10)

        try:
            consulta_sql = """SELECT * FROM  produtos ORDER BY estoque ASC LIMIT 1"""

            conexao_sql = db.conectar()
            cursor = conexao_sql.cursor()
            cursor.execute(consulta_sql)

            resultado = cursor.fetchall()
            if resultado:
                for linha in resultado:
                    print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")
            else:
                print("\nNenhum produto foi encontrado no banco de dados")
        
        except Error as e:
            print(f"\nErro ao conectar ao banco de dados: {e}")
    
        finally:
            db.desconectar(conexao_sql, cursor)
    
def produtoMaiorEstoque():
# Função para mostrar produto com maior estoque

    print("\n" +" -="*10 + " PRODUTO COM MAIOR ESTOQUE " + "-="*10)
    try:
        consulta_sql = """SELECT * FROM  produtos ORDER BY estoque DESC LIMIT 1"""

        conexao_sql = db.conectar()
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql)

        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                print(f"\nId: {linha[0]} | Nome: {linha[1]} | Preço: R${linha[2]:.2f} | Estoque: {linha[3]}un")
        else:
            print("\nNenhum produto foi encontrado no banco de dados")
    
    except Error as e:
        print(f"\nErro ao conectar ao banco de dados: {e}")

    finally:
        db.desconectar(conexao_sql, cursor)

def mediaEstoque():
# Função para mostrar a média de items no estoque

    try:
        consulta_sql = """
            SELECT AVG(estoque) AS media_estoque FROM produtos WHERE estoque > 0;"""
        conexao_sql = db.conectar()
        cursor = conexao_sql.cursor()
        cursor.execute(consulta_sql)
        
        resultado = cursor.fetchone()
        if resultado:
            print(f"A média total dos items no estoque é de {resultado[0]:.2f} unidades ")
        else:
            print("Nenhum produto foi cadastrado no sistema")
    
    except Error as e:
        print(f"\nErro ao conectar ao banco de dados: {e}")
    
    finally:
        db.desconectar(conexao_sql, cursor)

















    

