import time
import csv
from Database import conexao as db
from mysql.connector import Error

def registrar_log(usuario_id, operacao, tabela_afetada, id_registro, detalhes):
    # Função para inserir um registro na tabela logs_operacoes.
    
    conexao = db.conectar()
    if not conexao:
        print("Erro ao conectar para registrar log.")
        return
    cursor = conexao.cursor()
    try:
        sql = """
            INSERT INTO logs_operacoes 
            (usuario_id, operacao, tabela_afetada, id_registro, detalhes)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (usuario_id, operacao, tabela_afetada, id_registro, detalhes))
        conexao.commit()
    except Error as e:
        print(f"Erro ao registrar log: {e}")
    finally:
        db.desconectar(conexao, cursor)





def exibir_logs(logs):
    # Função para exibir logs

    if not logs:
        print("\nNenhum log encontrado.")
        return 
    print("\n" + "="*80)
    print(f"{'Data/Hora':<20} {'Usuário':<15} {'Operação':<8} {'Tabela':<15} {'ID':<5} Detalhes")
    print("="*80)
    for log in logs:
        data = log[0].strftime("%Y-%m-%d %H:%M:%S") if log[0] else ""
        print(f"{data:<20} {log[1]:<15} {log[2]:<8} {log[3]:<15} {log[4]:<5} {log[5]}")



def buscar_todos_logs(limite=100):
    # Função para buscar dados no banco de dados

    conexao = db.conectar()
    if not conexao:
        print("Erro de conexão.")
        return []
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT l.data_hora, u.nome, l.operacao, l.tabela_afetada, l.id_registro, l.detalhes
            FROM logs_operacoes l
            JOIN usuarios u ON l.usuario_id = u.id_usuario
            ORDER BY l.data_hora DESC
            LIMIT %s
        """, (limite,))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar logs: {e}")
        return []
    finally:
        db.desconectar(conexao, cursor)


def buscar_logs_acesso_auditoria():
    # Função que exibe logs de acesso ao menu de auditoria
    
    conexao = db.conectar()
    if not conexao:
        return []
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT l.data_hora, u.nome, l.detalhes
            FROM logs_operacoes l
            JOIN usuarios u ON l.usuario_id = u.id_usuario
            WHERE l.operacao = 'ACESSO' AND l.tabela_afetada = 'auditoria'
            ORDER BY l.data_hora DESC
            LIMIT 50
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar acessos: {e}")
        return []
    finally:
        db.desconectar(conexao, cursor)



def menuLogs():
    while True:
        print("-=-=-= MENU DE LOGS =-=-=-\n")
        print("[1] Ver logs completos")
        print("[2] Log de acessos à auditoria")
        print("[3] Voltar para menu inicial")
        try:
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    dados = buscar_todos_logs(100)
                    exibir_logs(dados)
                            
                case 2:
                    buscar_logs_acesso_auditoria()
                
                case 3:
                    print("\nRetornando...")
                    time.sleep(1.5)
                    return
                
                case _:
                    print("\nOpção inválida: digite um numero entre (1 - 4)")

        except ValueError:
            print("\nERRO: a opção precisa ser um numero inteiro válido")

