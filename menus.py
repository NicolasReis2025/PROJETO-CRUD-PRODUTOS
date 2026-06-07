from Crud import Adicionar, Atualizar, Buscar, Deletar, Listar
from Relatorio import DadosAnalisticos
import time
from Auditoria import menuAuditoria as auditoria
from Auditoria import auth

def menuInicial():
    while True:
        print("\n-=-=-=- MENU INICIAL -=-=-=-\n")
        print("[1] Menu principal")
        print("[2] Auditoria")
        print("[3] Sair")
        try:
            opcao = int(input("\nDigite uma opção: "))
            match opcao:
                case 1:
                    print("\nEntrando no menu Principal...")
                    time.sleep(1.5)
                    menuPrincipal()

                case 2:     
                    print("Entrando no menu de auditoria....")
                    time.sleep(1.5)
                    auditoria.menuAuditoria()

                case 3:
                    print("Encerrando programa.....")
                    time.sleep(1.5)
                    return

                case _:
                    print("\nOpção inválida: digite um numero entre (1 - 3)")

        except ValueError:
            print("\nERRO: a opção precisa ser um numero inteiro válido")


def menuPrincipal():
    while True:
        mostrarOpcoes()
        try:
            opcao = int(input("\nDigite uma opção: "))
        except ValueError:
            print("\nDigite apenas números!")
            continue    

        match opcao:
            case 1:
                Adicionar.cadastrarProduto()
            case 2:
                Atualizar.atualizarProduto()
            case 3:
                Buscar.buscarProduto()
            case 4:
                Deletar.deletarProduto()
            case 5:
                Listar.listarProdutos()
            case 6:
                print("\nRetornando....")
                time.sleep(1.5)
                return
            case _:
                print("\nOpção inválida....tente novamente")

def mostrarOpcoes():
        print(
        "\n[1] Adicionar produto"
        "\n[2] Atualizar produto"
        "\n[3] Buscar produto"
        "\n[4] Deletar produto"
        "\n[5] Listar produto" 
        "\n[6] Retornar para o menu inicial" 
        )
                  
