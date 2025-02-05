import os
import random

print("#########################################################################")
print("#########################################################################")
print("####################### Jogo do Campo Minado ############################")
print("#######################                      ############################")
print("####################### Por: Leandro Machado ############################")
print("#########################################################################")
print("#########################################################################")

ESCONDIDA = 0
PROXIMO = 1
MINA = 2
VAZIO = 3

TAMANHO_CAMPO = 16
PONTOS_REQUERIDOS = 0

DIRECOES = [
    (0, 1),  # Baixo
    (0, -1), # Cima
    (1, 0),  # Direita
    (-1, 0), # Esquerda
    (1, 1),  # Diagonal inferior direita
    (1, -1), # Diagonal superior direita
    (-1, 1), # Diagonal inferior esquerda
    (-1, -1) # Diagonal superior esquerda
]

pontuacao = 0
comando = ""

def limpar_tela():
    """Limpa a tela do terminal no Windows, Linux e macOS."""
    os.system("cls" if os.name == "nt" else "clear")

def escolha_valida(x, y):
        """Verifica se a coordenada está dentro do tabuleiro"""
        global TAMANHO_CAMPO
        return 0 <= x < TAMANHO_CAMPO and 0 <= y < TAMANHO_CAMPO

def montar_campos(tamanho_campo):
    campo_vazio = []
    campo_minado = []
    for _ in range(tamanho_campo):
        campo_vazio.append([ESCONDIDA for _ in range(tamanho_campo)])
        campo_minado.append([VAZIO for _ in range(tamanho_campo)])
    
    return campo_vazio, campo_minado


def minar_campo(campo_minado, tamanho_campo):
    global PONTOS_REQUERIDOS, PROXIMO, MINA, DIRECOES
    quantidade = random.randint(tamanho_campo - 6 if not tamanho_campo - 6 < 0 else 0, tamanho_campo - 1)
    PONTOS_REQUERIDOS = (tamanho_campo * tamanho_campo) - quantidade

    for i in range(quantidade):
        # Minar uma coordenada aleatória
        y = random.randint(0, tamanho_campo - 1)
        x = random.randint(0, tamanho_campo - 1)

        campo_minado[y][x] = MINA

        for dx, dy in DIRECOES:
            novo_x, novo_y = x + dx, y + dy
            if escolha_valida(novo_x, novo_y):
                if campo_minado[novo_y][novo_x] == MINA:
                    continue
                else:
                    campo_minado[novo_y][novo_x] = PROXIMO
    
    return campo_minado, PONTOS_REQUERIDOS

def print_campo(campo):
    str_colunas = ""
    print("Pontuação: ", pontuacao)
    print("")
    print("")
    print("Campo: ")
    print("")
    for i in range(TAMANHO_CAMPO):
        if i < 10:
            str_colunas += f"{i+1}  "
        else:
            str_colunas += f"{i+1} "
    print(f"    {str_colunas}") #TODO: AJUSTAR ESSE PRINT
    print("") #TODO: AJUSTAR ESSE PRINT
    for y in range(TAMANHO_CAMPO):
        print(f"{y+1}|", end=" ") #TODO: AJUSTAR ESSE PRINT
        for x in range(TAMANHO_CAMPO):
            if campo[y][x] == ESCONDIDA:
                print("■", end="  ")
            elif campo[y][x] == MINA:
                print("M", end="  ")
            elif campo[y][x] == VAZIO:
                print("0", end="  ")
            elif campo[y][x] == PROXIMO:
                print("1", end="  ")
            else:
                print(".", end="  ")
        print("")      
    print("")


def instrucoes():
    limpar_tela()
    print("Instruções:")
    print("Escolha uma posição para marcar uma célula (linha, coluna) ou digite SAIR para sair.")
    print("Você poderá ver números ao redor da célula, eles significam a distância para uma mina.")
    print(f"A pontuação necessária ganhar no tamanho do campo atual é: {PONTOS_REQUERIDOS}. Ou seja, todas as células sem minas.")
    print("Se você escolher uma célula com uma mina, perde o jogo.")
    print("")
    input("Aperte Enter para voltar ao Menu Principal!")

def escolher_tamanho_campo():
    limpar_tela()
    global TAMANHO_CAMPO

    print("Escolha um novo tamanho de campo:")
    tamanho_novo = input("Digite um número: ")
    if not tamanho_novo.isdigit():
        print("## Entrada inválida. Tente novamente. ##")
        return
    TAMANHO_CAMPO = int(tamanho_novo)


def jogar():
    limpar_tela()
    global pontuacao, TAMANHO_CAMPO, comando, DIRECOES

    campo_vazio, campo_minado = montar_campos(TAMANHO_CAMPO)
    campo_minado, pontos_requeridos_atual = minar_campo(campo_minado, TAMANHO_CAMPO)

    print("")
    print_campo(campo_vazio)
    print("")

    while comando != "SAIR":
        comando = input("Digite uma linha ou SAIR: ")

        if comando.upper() == "SAIR":
            break
        elif not comando.isdigit():
            print("## Comando inválido. Tente novamente. ##")
            continue

        comando = int(comando)

        if comando < 1 or comando > TAMANHO_CAMPO:
            print("## Linha inválida. Tente novamente. ##")
            continue

        linha = comando - 1



        comando = input("Digite uma coluna: ")

        if not comando.isdigit():
            print("## Comando inválido. Tente novamente. ##")
            continue

        comando = int(comando)

        if comando < 1 or comando > 4:
            print("## Coluna inválida. Tente novamente. ##")
            continue

        coluna = comando - 1



        if campo_minado[linha][coluna] == MINA:
            print("")
            print("#########################################################################")
            print("################# Você marcou um minado! Você perdeu...##################")
            print("#########################################################################")
            print("")
            campo_vazio[linha][coluna] = MINA
            print_campo(campo_vazio)
            break

        if campo_vazio[linha][coluna] == VAZIO or campo_vazio[linha][coluna] == PROXIMO:
            print("---- Você já marcou essa célula. Tente outra posição. -----")
            continue

        if campo_vazio[linha][coluna] == ESCONDIDA:
            if campo_minado[linha][coluna] == VAZIO:
                campo_vazio[linha][coluna] = VAZIO
            else:
                campo_vazio[linha][coluna] = PROXIMO

            qtd_minas_ao_redor = 0
            
            for dx, dy in DIRECOES:
                novo_x, novo_y = coluna + dx, linha + dy
                if escolha_valida(novo_x, novo_y):
                    if campo_minado[novo_y][novo_x] == MINA:
                        qtd_minas_ao_redor += 1
                        continue
                    elif campo_minado[novo_y][novo_x] == PROXIMO:
                        campo_vazio[novo_y][novo_x] = PROXIMO
                    elif campo_minado[novo_y][novo_x] == VAZIO:
                        campo_vazio[novo_y][novo_x] = VAZIO

            pontuacao += 8 - qtd_minas_ao_redor
            print_campo()
            if pontuacao == pontos_requeridos_atual:
                print("*************************************************************************")
                print("*********************** Parabéns! Você ganhou! **************************")
                print("*************************************************************************")
                break
    

while True:
    print("")
    print("Menu Principal:")
    print("1. Jogar")
    print("2. Instruções")
    print("3. Escolher tamanho do campo")
    print("0. Sair")
    print("")
    comando = input("Digite um número: ")

    if comando == "1":
        jogar()
    elif comando == "2":
        instrucoes()
    elif comando == "3":
        escolher_tamanho_campo()
    elif comando == "0":
        break

    