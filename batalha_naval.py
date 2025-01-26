# Batalha naval
import random
import os
import time

global pontuacao, pontuacao_computador, dificuldade_computador, PADRAO, AGUA, TIRO, BARCO, ultimo_tiro, campo_cliente, campo_cliente_computador, campo_computador, campo_computador_cliente
pontuacao = 0
pontuacao_computador = 0
dificuldade_computador = 2
PADRAO = 0
AGUA = 1
TIRO = 2
BARCO = 3
# Último tiro bem-sucedido do computador
ultimo_tiro = None

def limpar_tela():
    """Limpa a tela do terminal no Windows, Linux e macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def print_campo(campo, cliente=False):
    print("")
    print("   1 2 3 4 5 6 7 8 9 10")
    print("   --------------------")
    if cliente:
        for i in range(5):
            print(f"{i+1}|", end=" ")
            for j in range(10):
                if campo[i][j] == PADRAO:
                    print(".", end=" ")
                elif campo[i][j] == AGUA:
                    print(".", end=" ")
                elif campo[i][j] == TIRO:
                    print("X", end=" ")
                else:
                    print("B", end=" ")
            print()
    else:
        for i in range(5):
            print(f"{i+1}|", end=" ")
            for j in range(10):
                if campo[i][j] == PADRAO:
                    print("O", end=" ")
                elif campo[i][j] == AGUA:
                    print(".", end=" ")
                elif campo[i][j] == TIRO:
                    print("X", end=" ")
                else:
                    print("B", end=" ")
            print()

# Campo do cliente
campo_cliente = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# Campo que o cliente vai ver do computador
campo_cliente_computador = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Campo do computador
campo_computador = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# Campo que o computador vai ver do cliente
campo_computador_cliente = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def jogada_computador():
    global ultimo_tiro

    limpar_tela()
    def tiro_valido(x, y):
        """Verifica se a coordenada está dentro do tabuleiro e ainda não foi atingida."""
        return 0 <= x < 10 and 0 <= y < 5 and campo_computador_cliente[y][x] == PADRAO

    # Se já tivermos um último tiro bem-sucedido, tentar direções próximas
    if ultimo_tiro:
        x, y = ultimo_tiro
        direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Baixo, cima, direita, esquerda
        random.shuffle(direcoes)

        for dx, dy in direcoes:
            novo_x, novo_y = x + dx, y + dy
            if tiro_valido(novo_x, novo_y):
                return registrar_tiro(novo_x, novo_y)


    x = random.randint(0, 9)
    y = random.randint(0, 4)
    if tiro_valido(x, y):
        return registrar_tiro(x, y)

def jogada_cliente():
    def tiro_valido(x, y):
        """Verifica se a coordenada está dentro do tabuleiro e ainda não foi atingida."""
        return 0 <= x < 10 and 0 <= y < 5 and campo_cliente_computador[y][x] == PADRAO
    
    while True:
        print("Sua vez de jogar!!")
        print_campo(campo_cliente_computador)

        x = input("Escolha a coordenada x (1-10): ")
        y = input("Escolha a coordenada y (1-5): ")
        limpar_tela()

        try:
            x, y = int(x) - 1, int(y) - 1  # Ajuste para índice da matriz (0-based)
            
            if not (0 <= x < 10 and 0 <= y < 5):
                print("Coordenadas fora dos limites. Tente novamente.")
                continue
            
            if not tiro_valido(x, y):
                print("Você já atirou nesse local. Escolha outra coordenada.")
                continue

            return registrar_tiro(x, y, 2)

        except ValueError:
            print("Entrada inválida! Digite números inteiros entre 1-10 e 1-5.")

def registrar_tiro(x, y, tipo=1):
    """
    Executa o tiro no tabuleiro e atualiza o estado.
    
    Args:
        x (int): Coordenada x do tiro.
        y (int): Coordenada y do tiro.
        tipo (int): Tipo do jogador (1: Computador, 2: Cliente).

    Returns:
        tuple: Coordenadas do tiro.
    """
    global ultimo_tiro, pontuacao, pontuacao_computador

    if tipo == 2:
        if campo_computador[y][x] == BARCO:
            campo_cliente_computador[y][x] = BARCO
            campo_computador[y][x] = TIRO
            pontuacao += 1
        elif campo_computador[y][x] == TIRO:
            print("Você já atirou nesse local, tente novamente")
            return jogada_cliente()
        else:
            campo_cliente_computador[y][x] = AGUA
            campo_computador[y][x] = TIRO
        print("")
        print_campo(campo_cliente_computador)
        print("")
        time.sleep(2)
    else:
        if campo_cliente[y][x] == BARCO:
            campo_computador_cliente[y][x] = BARCO
            campo_cliente[y][x] = TIRO
            pontuacao_computador += 1
            ultimo_tiro = (x, y)  # Armazena para a próxima rodada
        elif campo_cliente[y][x] == TIRO:
            return registrar_tiro(x, y)
        else:
            campo_computador_cliente[y][x] = AGUA
            campo_cliente[y][x] = TIRO
            ultimo_tiro = None  # Se errar, volta a atirar aleatoriamente
        print(f"Computador jogou nas coordenadas: {x + 1}, {y + 1}")
        print("")
        print_campo(campo_cliente, True)
        print("")
        time.sleep(2)

    return x, y

def barcos_computador():
    """Coloca os barcos do computador no tabuleiro."""
    barcos = dificuldade_computador
    while barcos > 0:
        x = random.randint(0, 9)
        y = random.randint(0, 4)
        direcao = random.randint(0, 1) # Vertical ou horizontal
        if direcao == 0:  # Vertical
            if (
                y + 3 < 4
                and campo_computador[y + 2][x] == PADRAO
                and campo_computador[y + 1][x] == PADRAO
                and campo_computador[y][x] == PADRAO
                ):
                campo_computador[y][x] = BARCO
                barcos -= 1
                for i in range(1, 3):
                    campo_computador[y + i][x] = BARCO
        else:  # Horizontal
            if (
                x + 3 < 9
                and campo_computador[y][x + 2] == PADRAO
                and campo_computador[y][x + 1] == PADRAO
                and campo_computador[y][x] == PADRAO
                ):
                campo_computador[y][x] = BARCO
                barcos -= 1
                for i in range(1, 3):
                    campo_computador[y][x + i] = BARCO

def barcos_cliente():
    """Coloca os barcos do cliente no tabuleiro."""
    limpar_tela()
    global dificuldade_cliente
    n_barcos_cliente = 1
    dificuldade_cliente = n_barcos_cliente
    while n_barcos_cliente > 0:
        print_campo(campo_cliente, True)
        print("Coloque um novo barco!")
        print(f"Barcos disponíveis: {n_barcos_cliente}")
        print("Escolha uma direção:")
        print("1 - Vertical")
        print("2 - Horizontal")
        print("")
        comando = input("Escolha um número: ")
        
        if comando not in ["1", "2"]:
            print("Comando inválido. Tente novamente.")
            continue
        elif comando == "1":
            direcao = 0
        elif comando == "2":
            direcao = 1
        else:
            direcao = 0
            print("Comando inválido. Tente novamente.")
            continue

        x = input("Escolha a coordenada x do barco: ")
        y = input("Escolha a coordenada y do barco: ")
        limpar_tela()
        try:
            x, y = int(x), int(y)
            x -= 1
            y -= 1
            if 0 > x > 9 and 0 > y > 4:
                print("Coordenadas inválidas. Tente novamente.")
                continue
        except ValueError:
            print("Coordenadas inválidas. Tente novamente.")
            continue


        if direcao == 0:  # Vertical
            if (
                y + 2 <= 4
                and campo_cliente[y + 2][x] == PADRAO
                and campo_cliente[y + 1][x] == PADRAO
                and campo_cliente[y][x] == PADRAO
                ):
                campo_cliente[y][x] = BARCO
                n_barcos_cliente -= 1
                for i in range(1, 3):
                    campo_cliente[y + i][x] = BARCO
            else:
                print("### Não é possível construir o barco. Tente novamente. ###")
                print("")
        else:  # Horizontal
            if (
                x + 2 <= 9
                and campo_cliente[y][x + 2] == PADRAO
                and campo_cliente[y][x + 1] == PADRAO
                and campo_cliente[y][x] == PADRAO
                ):
                campo_cliente[y][x] = BARCO
                n_barcos_cliente -= 1
                for i in range(1, 3):
                    campo_cliente[y][x + i] = BARCO
            else:
                print("### Não é possível construir o barco. Tente novamente. ###")
                print("")

def instrucoes():
    limpar_tela()
    print("Instruções:")
    print("Escolha uma dificuldade, quanto maior, mais barcos o computador terá.")
    print("Após isso, você escolherá onde seu barco ficará.")
    print("Caso escolha vertical, escolha uma opção e o barco será construído dessa mesma célula para baixo.")
    print("Caso escolha horizontal, escolha uma opção e o barco será construído dessa mesma célula para direita.")
    print("Escolha uma posição para marcar um minado (linha, coluna) ou digite SAIR para sair.")
    print("")

def escolher_dificuldade():
    limpar_tela()
    print("Escolha uma dificuldade")
    print("1. Fácil")
    print("2. Normal")
    print("3. Difícil")
    print("")
    global dificuldade_computador
    dificuldade = input("Digite um número: ")
    if dificuldade == "1":
        dificuldade_computador = 1
    elif dificuldade == "2":
        dificuldade_computador = 2
    elif dificuldade == "3":
        dificuldade_computador = 3
    else:
        print("Dificuldade inválida..")
        escolher_dificuldade()
    limpar_tela()

def jogar():
    barcos_computador()
    barcos_cliente()

    global pontuacao, dificuldade_computador, dificuldade_cliente
    comando = ""
    limpar_tela()


    while True:
        if comando == "SAIR" or comando == "sair":
            break

        jogada_cliente()
        jogada_computador()
        
        print(f"Sua pontuação é: {pontuacao}/{dificuldade_computador * 3}")
        
        if pontuacao == dificuldade_computador * 3:
            print("#########################################################################")
            print("#########################################################################")
            print("##################### Parabéns, você venceu! ############################")
            print("#########################################################################")
            print("#########################################################################")
            break

        if pontuacao_computador == dificuldade_cliente * 3:
            print("#########################################################################")
            print("##################### Game Over, você perdeu! ###########################")
            print("#####################                         ###########################")
            print(f"#####################     Pontuação: {pontuacao}       ###########################")
            print("#########################################################################")
            print("#########################################################################")
            break
        
        comando = input("Sua vez, aperte ENTER para jogar ou digite SAIR para encerrar")
        

    

def main():
    print("#########################################################################")
    print("#########################################################################")
    print("######################  Jogo da Batalha Naval ###########################")
    print("######################                        ###########################")
    print("######################  Por: Leandro Machado  ###########################")
    print("#########################################################################")
    print("#########################################################################")
    print("")
    comando = ""
    # Menu principal
    while comando != "1":
        print("Menu Principal:")
        print("1. Jogar")
        print("2. Instruções")
        print("3. Escolher dificuldade")
        print("0. Sair")
        print("")
        comando = input("Digite um número: ")
        if comando == "1":
            jogar()
        elif comando == "2":
            instrucoes()
        elif comando == "3":
            escolher_dificuldade()
        elif comando == "0":
            print("Saindo...")
            return
        else:
            print("Comando inválido. Tente novamente.")

main()