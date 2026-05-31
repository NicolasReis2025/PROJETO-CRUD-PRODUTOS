from Database import conexao as db
from mysql.connector import Error
import time
from Auditoria import auth
from Auditoria import logs

def deletarProduto():
    # Função para deletar produto

    print("=-"*10 + " DELETAR PRODUTO " + "=-"*10)

    while True:
        try:
            produto_id = int(input("\nDigite o id do produto para removê-lo: "))
            break
        except ValueError:
            print("\nERRO: entrada inválida. Digite um número inteiro.")
            continue

    conexao_sql = db.conectar()
    if conexao_sql is None:
        print("Falha na conexão com o banco.")
        return

    cursor = conexao_sql.cursor()
    try:
        cursor.execute("SELECT nome, preco, estoque FROM produtos WHERE id_produto = %s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            print("\nNenhum produto cadastrado com esse id no banco de dados.")
            return

        print(f"\nId: {produto_id} | Nome: {produto[0]} | Preço: R${produto[1]:.2f} | Estoque: {produto[2]}un")

        while True:
            try:
                print("\nDeseja realmente deletar esse produto?")
                print("[1] Sim\n[2] Não")
                confirmacao = int(input("Digite uma opção: "))
                if confirmacao == 1:
                    remover_sql = "DELETE FROM produtos WHERE id_produto = %s"
                    cursor.execute(remover_sql, (produto_id,))
                    conexao_sql.commit()

                    if cursor.rowcount > 0:
                        detalhes = f"nome: {produto[0]}, preco: {produto[1]:.2f}, estoque: {produto[2]}"
                        logs.registrar_log(auth.usuario_logado['id'], 'DELETE', 'produtos', produto_id, detalhes)
                        print("\nProduto removido com sucesso!")
                    else:
                        print("\nNenhum produto foi removido (ID não encontrado).")
                        time.sleep(0.5)
                        print("\nRetornando")
                        time.sleep(1.5)
                        return

                elif confirmacao == 2:
                    print("\nRetornando para o menu Principal.....")
                    time.sleep(1.5)
                    return
                else:
                    print("ERRO: opção inválida. Digite 1 para SIM ou 2 para NÃO.")
            except ValueError:
                print("\nEntrada inválida. Digite um número.")

    except Error as e:
        print(f"\nErro no banco de dados: {e}")
    finally:
        db.desconectar(conexao_sql, cursor)