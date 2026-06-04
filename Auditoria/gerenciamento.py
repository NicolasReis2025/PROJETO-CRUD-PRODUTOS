import string

from Database import conexao as db
from Auditoria import auth
from mysql.connector import Error
import time
import bcrypt
from Auditoria import logs
import random

def listar_usuarios():
    # Função de listar usuários

    if not auth.is_admin():
        print("\nAcesso negado")
        return
    conexao = db.conectar()
    cursor = conexao.cursor()

    try:
        consulta_sql = "SELECT * FROM usuarios"
        cursor.execute(consulta_sql)
        resultado = cursor.fetchall()
        
        if not resultado:
            print("\nNão há usuários cadastrados no banco de dados")
            return
        
        print("\n-=-=-= LISTA DE USUÁRIOS -=-=-=-=")
        for u in resultado:
            print(f"ID: {u[0]} | Nome: {u[1]} | Login: {u[2]} | Perfil: {u[3]}")
    
    except Error as e:
        print(f"Erro: {e}")

    finally:
        db.desconectar(conexao, cursor)




def alterar_perfil():
    # Função para alterar perfil do usuário

    if not auth.is_admin():
        print("\nAcesso negado")
        return

    print("\n-=-=-= LISTA DE USUÁRIOS -=-=-=-=\n")
    listar_usuarios()

    while True:
        try:
            usuario_id = int(input("\nDigite o ID do usuário que deseja alterar o perfil: "))
            
            if usuario_id == auth.usuario_logado['id']:
                print("Você não pode alterar seu próprio perfil.")
                time.sleep(1)
                print("\nRetornando.....")
                time.sleep(0.8)
                return

            break     

        except ValueError:
            print("ID inválido. Digite um número inteiro.")

        
    try:
        conexao = db.conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id_usuario, nome, perfil FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            print(f"Usuário com ID {usuario_id} não encontrado.")
            time.sleep(1)
            print("\nRetornando.....")
            time.sleep(0.8)
            return

        print(f"\nUsuário selecionado: {usuario[1]} (perfil atual: {usuario[2]})")
        
        while True:
                print("\n-=-=-=- OPÇÃO PARA ATUALIZAÇÃO DO NOVO PERFIL -=-=-=-\n")
                print("[1] Admin")
                print("[2] Operador")

                opcao_perfil = int(input("Digite uma opção: "))
                match opcao_perfil:
                    case 1:
                        novo_perfil = "admin"
                        break

                    case 2:
                        novo_perfil = "operador"
                        break
                    
                    case _:
                        print("\nERRO: a opão precisa ser um numero entre (1~2) ")
                        

        
        if novo_perfil == usuario[2]:
            print(f"O usuário já possui o perfil '{novo_perfil}'. Nenhuma alteração feita.")
            time.sleep(1)
            print("\nRetornando.....")
            return

        cursor.execute("UPDATE usuarios SET perfil = %s WHERE id_usuario = %s", (novo_perfil, usuario_id))
        conexao.commit()

        print(f"\nPerfil do usuário {usuario[1]} alterado de '{usuario[2]}' para '{novo_perfil}' com sucesso!")


        logs.registrar_log(
            auth.usuario_logado['id'],
            'UPDATE',
            'usuarios',
            usuario_id,
            f"Perfil alterado de {usuario[2]} para {novo_perfil}"
        )

    except Error as e:
        print(f"Erro ao alterar perfil: {e}")
    finally:
        db.desconectar(conexao, cursor)



def gerar_senha_aleatoria(tamanho=10):
    caracteres = string.ascii_letters + string.digits + "!@#$%*"
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

def redefinirSenha():

    if not auth.is_admin():
        print("\nAcesso negado")
        return

    while True:
        try:
            id_usuario = int(input("\nDigite o id do usuário: "))
            
            conexao_temp = db.conectar()
            if not conexao_temp:
                print("Erro de conexão com o banco.")
                return
            cursor_temp = conexao_temp.cursor()
            
            cursor_temp.execute("SELECT id_usuario, nome, perfil FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            resultado = cursor_temp.fetchall()
            
            if not resultado:
                print("\nUsuário não encontrado na base de dados")
                time.sleep(1.5)
                print("\nRetornando....")
                time.sleep(1)
                db.desconectar(conexao_temp, cursor_temp) 
                return

            for linha in resultado:
                print(f"\nId: {linha[0]} | Nome: {linha[1]} | Perfil: {linha[2]}")

            print("\nDeseja realmente redefinir a senha desse usuário?")
            print("\n[1] Sim\n[2] Não")
            opcao = int(input("\nDigite a uma opção: "))
            match opcao:
                case 1:
                    db.desconectar(conexao_temp, cursor_temp) 
                    break
                case 2:
                    print("\nRetornando....")
                    time.sleep(1.5)
                    db.desconectar(conexao_temp, cursor_temp)
                    return
                case _:
                    print("\nERRO: a opção deve ser um numero entre (1 ~ 2)")
                    db.desconectar(conexao_temp, cursor_temp)
                    continue

        except ValueError:
            print("\nEntrada inválida. Tente novamente!")
        except Error as e:
            print(f"\nErro no banco de dados: {e}")
            
    while True:
        print("\n[1] criar manualmente")
        print("[2] Gerar senha aleatória")
        print("[3] Sair")
        try:
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    while True:
                        senha1 = str(input("\nDigite a nova senha: "))
                        senha2 = str(input("\nDigite a senha novamente: "))
                        if senha1 != senha2:
                            print("\nERRO: as senhas não coincidem")
                            continue
                        if len(senha1) < 4:
                            print("A senha deve ter pelo menos 4 caracteres.")
                            continue
                        nova_senha_plana = senha1
                        metodo = 1   
                        break
                    break  

                case 2:
                    nova_senha_plana = gerar_senha_aleatoria(10)
                    print(f"\nSenha gerada: **{nova_senha_plana}**")
                    print("Anote esta senha e entregue ao usuário.")
                    print("\nConfirmação de redefinição de senha: ")
                    while True:
                        try:
                            print("\n[1] Sim\n[2] Não")
                            confirmacao = int(input("\nDigite uma opção: "))
                            match confirmacao:
                                case 1:
                                    metodo = 2   
                                    break
                                case 2:
                                    print("\nRetornando....")
                                    time.sleep(1.5)
                                    return
                                case _:
                                    print("\nERRO: opção inválida")
                        except ValueError:
                            print("\nERRO: digite um número inteiro")
                    break   
                case 3:
                    print("\nRetornando....")
                    time.sleep(1.5)
                    return
        except ValueError:
            print("\nERRO: a opção precisa ser um número inteiro válido")


    novo_hash = bcrypt.hashpw(nova_senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    conexao = db.conectar()
    if not conexao:
        print("Erro de conexão. Senha não foi alterada.")
        return
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE usuarios SET senha_hash = %s WHERE id_usuario = %s", (novo_hash, id_usuario))
        conexao.commit()
        if cursor.rowcount > 0:
            print("\n✅ Senha redefinida com sucesso!")
            logs.registrar_log(
                auth.usuario_logado['id'],
                'UPDATE',
                'usuarios',
                id_usuario,
                f"Senha redefinida (método: {'manual' if metodo == 1 else 'aleatório'})"
            )
        else:
            print("\n❌ Falha ao redefinir a senha (usuário não encontrado).")
    except Error as e:
        print(f"Erro ao atualizar senha: {e}")
    finally:
        db.desconectar(conexao, cursor)



def menuGerenciamento():
    while True:
        print("\n-=-=-= MENU DE GERENCIAMENTO -=-=-=-\n")
        print("[1] Listar usuários")
        print("[2] Alterar usuários")
        print("[3] Redefinir senha")
        print("[4] Voltar para menu inicial")
        try:
            opcao = int(input("Digite uma opção: "))
            match opcao:
                case 1:
                    listar_usuarios()
                case 2:
                    alterar_perfil()
                case 3:
                    redefinirSenha()
                case 4:
                    print("\nRetornando....")
                    time.sleep(1.5)
                    return
                case _:
                    print("\nErro: a opção precisa ser um numero entre (1~ 4)")
        except ValueError:
            print("\nERRO: a opção precisa ser um numero inteiro válido")
        
