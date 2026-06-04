import time
from Relatorio import DadosAnalisticos as estatistica
from Auditoria import logs
from Auditoria import exportacao
from Auditoria import auth
from Auditoria import gerenciamento

def menuAuditoria():
    while True:
        print("-=-=-= MENU AUDITORIA =-=-=\n")
        print("[1] Ver Logs")
        print("[2] Exportar csv")
        print("[3] Relatórios estátisticos")
        print("[4] Gerenciamento de usuários")
        print("[5] Voltar para o menu inicial")
        try:
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    print("Entrando no menu de logs.....")
                    time.sleep(1.5)
                    logs.menuLogs()
                
                case 2:
                    print("Entrando no menu de exportação em csv.....")
                    time.sleep(1.5)
                    exportacao.menuCsv()   

                case 3:
                    print("Entrando no menu de estátisticas.....")
                    time.sleep(1.5)
                    estatistica.menuRelatorio()
                
                case 4:
                    if not auth.is_admin():
                        print("\nAcesso negado")
                        time.sleep(0.8)
                        continue
                    
                    gerenciamento.menuGerenciamento()

                case 5:
                    print("\nRetornando...")
                    time.sleep(1.5)
                    return

                case _:
                    print("\nOpção inválida: digite um numero entre (1 - 4)")

        except ValueError:
            print("\nERRO: a opção precisa ser um numero inteiro válido")

