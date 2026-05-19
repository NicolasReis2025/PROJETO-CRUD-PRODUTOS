from Database import conexao as db
from mysql.connector import Error
import time

def atualizarProduto():
    # Função para atualizar produto

    print("=-"*10 + " ATUALIZAR PRODUTO " + "=-" * 10)

    while True:
        try:
            produto_id = int(input("\nDigite o id do produto que deseja atualizar: "))
            break
        except ValueError:
            print("\nERRO: entrada inválida. Digite um número inteiro.")
            continue

    conexao = None
    cursor = None

    try:
        conexao = db.conectar()
        if conexao is None:
            print("Falha na conexão com o banco.")
            return

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id_produto = %s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print("\nNenhum produto foi encontrado com esse ID.")
            return

        print(f"\nId: {produto[0]} | Nome: {produto[1]} | Preço: R${produto[2]:.2f} | Estoque: {produto[3]}un")

        while True:
            try:
                print("\nDeseja realmente atualizar este produto?")
                print("\n[1] Sim\n[2] Não")
                confirmar = int(input("Digite uma opção: "))
                match confirmar:
                    case 1:
                        break
                    case 2:
                        print("\nRetonando ao menu principal...")
                        time.sleep(1.5)
                        return
                    case _:
                        print("ERRO: opção deve ser um numero entre 1 e 2. Tente novamente!")
                        
            except ValueError:
                print("Entrada inválida. Digite um número.")

        while True:
            try:
                nome = input("Digite o novo nome do produto: ").strip()
                if not nome:
                    print("O nome não pode estar vazio.")
                    continue
                preco = float(input(f"Digite o novo preço do(a) '{nome}': "))
                if preco < 0:
                    print("Preço não pode ser negativo.")
                    continue
                estoque = int(input("Digite a nova quantidade em estoque: "))
                if estoque < 0:
                    print("Estoque não pode ser negativo.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. Use números para preço e estoque.")


        print("\nNovos dados do produto:")
        print(f"Nome: {nome}")
        print(f"Preço: R${preco:.2f}")
        print(f"Estoque: {estoque} unidades")
      

        sql = "UPDATE produtos SET nome=%s, preco=%s, estoque=%s WHERE id_produto=%s"
        cursor.execute(sql, (nome, preco, estoque, produto_id))
        conexao.commit()

        if cursor.rowcount == 0:
            print("\nNenhum produto foi atualizado (ID não encontrado).")
        else:
            print("\nProduto atualizado com sucesso!")

    except Error as e:
        print(f"\nErro no banco de dados: {e}")
        
    finally:
        db.desconectar(conexao, cursor)