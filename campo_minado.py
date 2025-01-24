import random
# CAMPO MINADO

campo_vazio = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

campo_minado = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

pontuacao = 0
comando = ""

def minar_campo():
    # Minar uma coordenada aleatória
    linha = random.randint(0, 3)
    coluna = random.randint(0, 3)

    campo_minado[linha][coluna] = 2

def print_campo():
    print("Pontuação: ", pontuacao)
    print("Campo: ")
    print("")
    for y in range(4):
        for x in range(4):
            if campo_vazio[y][x] == 0:
                print("O", end=" ")
            elif campo_vazio[y][x] == 2:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print("")      
    print("")

minar_campo()

print("#########################################################################")
print("#########################################################################")
print("####################### Jogo do Campo Minado ############################")
print("#######################                      ############################")
print("####################### Por: Leandro Machado ############################")
print("#########################################################################")
print("#########################################################################")
print("")
print("Instruções:")
print("Escolha uma posição para marcar um minado (linha, coluna) ou digite SAIR para sair.")
print("")
print_campo()
print("")
print("")





while comando != "SAIR":
    comando = input("Digite uma linha ou SAIR: ")

    if comando.upper() == "SAIR":
        break

    try:
        comando = int(comando)
        if comando < 1 or comando > 4:
            print("## Linha inválida. Tente novamente. ##")
            continue
        linha = comando - 1
        comando = input("Digite uma coluna: ")
        comando = int(comando)
        if comando < 1 or comando > 4:
            print("## Coluna inválida. Tente novamente. ##")
            continue
        coluna = comando - 1
        if campo_minado[linha][coluna] == 2:
            print("")
            print("#########################################################################")
            print("################# Você marcou um minado! Você perdeu...##################")
            print("#########################################################################")
            print("")
            campo_vazio[linha][coluna] = 2
            pontuacao -= 10
            print_campo()
            break
        if campo_vazio[linha][coluna] == 1:
            print("---- Você já marcou esse minado. Tente outra posição. -----")
            continue
        if campo_vazio[linha][coluna] == 0:
            campo_vazio[linha][coluna] = 1
            pontuacao += 10
            print_campo()
            if pontuacao == 150:
                print("#########################################################################")
                print("####################### Parabéns! Você ganhou! ##########################")
                print("#########################################################################")
                break

    except ValueError:
        print("## Comando inválido. Tente novamente. ##")
        continue


    