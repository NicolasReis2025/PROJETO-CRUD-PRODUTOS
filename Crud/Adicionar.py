from Database import conexao as db
from mysql.connector import Error
from Auditoria import auth
from Auditoria import logs
import time

def cadastrarProduto():
    # Função para cadastrar produto

    while True:
        try:
            nome = str(input("\nDigite o nome do produto: ")).strip()
            if not nome or not any(c.isalpha() for c in nome):
                print("ERRO: o nome precisa ter pelo menos uma letra")
                continue

            preco = float(input(f"Digite o preço do(a) '{nome}': "))
            if preco < 0:
                print("\nErro: o preço não pode ser um valor negativo. Tente novamente!\n")
                continue

            estoque = int(input("Digite a quantidade em estoque: "))
            if estoque < 0:
                    print("\nErro: a quantidade em estoque não pode ser um numero negativo. Tente novamente!\n")
                    continue
            break

        except ValueError:
            print("\nERRO: entrada inválida. Tente novamente!\n")
            continue
    

    print(f"\n\nNome: {nome} | Preço: R${preco:.2f} | estoque: {estoque} unidades")
    while True:
            try:
                print("\n\nDeseja realmente adicionar esse produto? ")
                print(
                    "\n[1] Sim" 
                    "\n[2] Não" 
                )
                opcao = int(input("Digite uma opção: "))
                match opcao:
                    case 1:
                        break
                    case 2:
                        print("\nRetornando......")
                        time.sleep(1.5)
                        return
                    case _:
                        print("\nERRO: a opção precisa ser um numero entre 1 (Sim) e 2 (Não) ")

            except ValueError:
                print("\nERRO: entrada inválida. Tente novamente!\n")
                continue 

    conexao_sql = db.conectar()
    if conexao_sql is None:
        print("Falha na conexão com o banco.")
        return
    
    cursor = conexao_sql.cursor()

    try:
        verificacao = "SELECT COUNT(*) FROM produtos WHERE LOWER(nome) = LOWER(%s)"
        cursor.execute(verificacao, (nome, ))
        count = cursor.fetchone()[0]
       
        if count == 0:
            sql = " INSERT INTO produtos(nome, preco, estoque) VALUES (%s, %s, %s);"
            valores = (nome, preco, estoque)
            cursor.execute(sql, valores)
            conexao_sql.commit()
            if cursor.rowcount == 0:
                print("Erro ao cadastrar produto")
            else:
                id_inserido = cursor.lastrowid   # pega o ID gerado
                detalhes = f"nome: {nome}, preco: {preco:.2f}, estoque: {estoque}"
                logs.registrar_log(auth.usuario_logado['id'], 'INSERT', 'produtos', id_inserido, detalhes)
                print("\nProduto cadastrado com sucesso!")

        else:
            print("\nProduto já cadastrado no banco de dados")

    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    finally:
        db.desconectar(conexao_sql, cursor)


