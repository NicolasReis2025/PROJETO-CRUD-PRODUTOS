from Crud import Adicionar, Atualizar, Buscar, Deletar, Listar
from Relatorio import DadosAnalisticos
import time

def mostrarOpcoes():
        print(
        "\n[1] Adicionar produto"
        "\n[2] Atualizar produto"
        "\n[3] Buscar produto"
        "\n[4] Deletar produto"
        "\n[5] Listar produto" 
        "\n[6] Relatórios" 
        "\n[7] Sair"
        )


def menuInicial():
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
                DadosAnalisticos.menuRelatorio()
            case 7:
                print("\nPrograma encerrando....")
                time.sleep(1.5)
                return
            case _:
                print("\nOpção inválida....tente novamente")
                  
