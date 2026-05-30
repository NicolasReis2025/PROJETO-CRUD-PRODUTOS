import time


def menuLogs():
    while True:
        print("[1] Ver logs completos")
        print("[2] Filtrar logs")
        print("[3] Log de acessos à auditoria")
        print("[4] Voltar para menu inicial")
        try:
            opcao = int(input("\nDigite uma opção: "))
        except ValueError:
            print("\nERRO: a opção precisa ser um numero inteiro válido")

