from Database import conexao as db
from mysql.connector import Error
import time
from Auditoria import auth
from Auditoria import logs

def atualizarProduto():
    # Função para atualizar produto
    print("=-"*10 + " ATUALIZAR PRODUTO " + "=-" * 10)

    while True:
        try:
            produto_id = int(input("\nDigite o id do produto que deseja atualizar: "))
            break
        except ValueError:
            print("\nERRO: entrada inválida. Digite um número inteiro.")

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
                print("[1] Sim\n[2] Não")
                confirmar = int(input("Digite uma opção: "))
                if confirmar == 1:
                    break
                elif confirmar == 2:
                    print("\nRetornando....")
                    time.sleep(1.5)
                    return
                else:
                    print("ERRO: opção inválida. Digite 1 ou 2.")
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
            detalhes = f"nome: {produto[1]} -> {nome}, preco: {produto[2]:.2f} -> {preco:.2f}, estoque: {produto[3]} -> {estoque}"
            logs.registrar_log(auth.usuario_logado['id'], 'UPDATE', 'produtos', produto_id, detalhes)
            print("\nProduto atualizado com sucesso!")

    except Error as e:
        print(f"\nErro no banco de dados: {e}")
    finally:
        db.desconectar(conexao, cursor)