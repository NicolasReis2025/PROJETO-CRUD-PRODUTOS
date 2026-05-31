import bcrypt
import time
from Database import conexao as db
from mysql.connector import Error


usuario_logado = None

def verificar_acesso():
    # Função para verificar se há um usuário

    global usuario_logado
    if usuario_logado is not None:
        return True
    return fazer_login()

def fazer_login():
    # função de exibir o menu de login/cadastro e autentica o usuário
    global usuario_logado

    while True:
        print("\n" + "="*40)
        print("      ACESSO RESTRITO - AUDITORIA")
        print("="*40)
        print("[1] Fazer login")
        print("[2] Cadastrar novo usuário")
        print("[3] Sair")
        try:
            opcao = int(input("Digite uma opção: "))
            match opcao:
                case 1:
                    usuario_logado = autenticar_usuario()
                    if usuario_logado:
                        print(f"\nBem-vindo, {usuario_logado['nome']}!")
                        time.sleep(1.5)
                        return True
                    else:
                        print("\nLogin ou senha inválidos. Tente novamente.")
                        time.sleep(1.5)

                case 2:
                    cadastrar_usuario()
                
                case 3:
                    print("\nRetornando....")
                    time.sleep(1.5)
                    return False
                case _:
                    print("\nERRO: a opção precisar ser um numero entre (1~3)")
        except ValueError:
            print("\nEntrada inválida. Digite um número inteiro válido.")
            continue


def autenticar_usuario():
    # Função que solicita login e senha

    login = str(input("Login: ")).strip()
    senha = str(input("Senha: ")).strip()

    conexao = db.conectar()
    if not conexao:
        print("\nErro de conexão com o banco.")
        return None
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_usuario, nome, senha_hash, perfil FROM usuarios WHERE login = %s", (login,))
        usuario = cursor.fetchone()
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario[2].encode('utf-8')):
            return {'id': usuario[0], 'nome': usuario[1], 'perfil': usuario[3]}
        return None
    except Error as e:
        print(f"\nErro ao autenticar: {e}")
        return None
    finally:
        db.desconectar(conexao, cursor)

def cadastrar_usuario():
    # Função de criar um novo usuário

    print("\n-=-=-= CADASTRO DE NOVO USUÁRIO -=-=-=-\n")
    nome = str(input("Nome completo: ")).strip()
    login = str(input("Login (nome de usuário): ")).strip()
    senha = str(input("Senha: ")).strip()
    confirma = str(input("Confirme a senha: ")).strip()

    if senha != confirma:
        print("\nERRO: as senhas não coincidem.")
        return
    if len(senha) < 4:
        print("\nERRO: a senha deve ter pelo menos 4 caracteres.")
        return

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt(rounds=5)).decode('utf-8')
    perfil = 'operador'   

    conexao = db.conectar()
    if not conexao:
        print("\nErro de conexão.")
        return
    cursor = conexao.cursor()
    try:
       
        cursor.execute("SELECT id_usuario FROM usuarios WHERE login = %s", (login,))
        if cursor.fetchone():
            print("\nEste login já está em uso. Escolha outro.")
            return
        cursor.execute(
            "INSERT INTO usuarios (nome, login, senha_hash, perfil) VALUES (%s, %s, %s, %s)",
            (nome, login, senha_hash, perfil)
        )
        conexao.commit()
        print("\nUsuário cadastrado com sucesso! Agora faça login.")
    except Error as e:
        print(f"\nErro ao cadastrar: {e}")
    finally:
        db.desconectar(conexao, cursor)


