import pygame
import sys
from collections import deque
import random

pygame.init()

# ================= CONFIG =================
TAMANHO = 24

# ======= SEU MAPA =======
mapa = [
    [1] * 25,
    [1] + [0] * 23 + [1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1] + [0] * 23 + [1],
    [1, 1] + [0] * 21 + [1, 1],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [1, 1] + [0] * 21 + [1, 1],
    [0, 0, 0] + [1, 0] * 9 + [1, 0, 0, 0],
    [0, 0, 0] + [1, 0] * 9 + [1, 0, 0, 0],
    [1, 1] + [0] * 21 + [1, 1],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [0, 1] + [0] * 21 + [1, 0],
    [1, 1] + [0] * 21 + [1, 1],
    [1] + [0] * 23 + [1],
    [1] + [0] * 23 + [1],
    [1] + [0] * 23 + [1],
    [1] * 25,
]

LINHAS = len(mapa)
COLUNAS = len(mapa[0])

LARGURA = COLUNAS * TAMANHO
ALTURA = LINHAS * TAMANHO

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man Corrigido")

font = pygame.font.SysFont("Arial", 20)
font_big = pygame.font.SysFont("Arial", 50)
clock = pygame.time.Clock()

# ================= CORES =================
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL_FRACO = (100, 100, 255)

# ================= POWER PELLETS =================
mapa[1][1] = 3
mapa[1][23] = 3
mapa[28][1] = 3
mapa[28][23] = 3

# ================= PACMAN =================
pac_x, pac_y = 1, 1
direcao = (0, 0)
proxima_direcao = (0, 0)
pontuacao = -50
vidas = 3
power = False
power_timer = 0
fantasmas_comidos = 0

# ================= FANTASMA =================
fantasma = {"x": 23, "y": 28}


# ================= BFS =================
def bfs(inicio, fim):
    fila = deque([inicio])
    visitado = {inicio: None}

    while fila:
        atual = fila.popleft()
        if atual == fim:
            caminho = []
            while atual:
                caminho.append(atual)
                atual = visitado[atual]
            return caminho[::-1]

        x, y = atual
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
                if mapa[ny][nx] != 1 and (nx, ny) not in visitado:
                    fila.append((nx, ny))
                    visitado[(nx, ny)] = atual
    return []


# ================= MOVIMENTO PACMAN =================
def mover_pacman():
    global pac_x, pac_y, pontuacao, power, power_timer
    global fantasmas_comidos, direcao, proxima_direcao

    # tenta virar
    nx = pac_x + proxima_direcao[0]
    ny = pac_y + proxima_direcao[1]

    if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
        if mapa[ny][nx] != 1:
            direcao = proxima_direcao

    # move
    nx = pac_x + direcao[0]
    ny = pac_y + direcao[1]

    if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
        if mapa[ny][nx] != 1:
            pac_x, pac_y = nx, ny

            if mapa[ny][nx] == 0:
                mapa[ny][nx] = 2
                pontuacao += 10

            if mapa[ny][nx] == 3:
                mapa[ny][nx] = 2
                pontuacao += 50
                power = True
                power_timer = pygame.time.get_ticks()
                fantasmas_comidos = 0


# ================= MOVIMENTO FANTASMA =================
def mover_fantasma():
    global pontuacao, power, fantasmas_comidos

    if power:
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nx = fantasma["x"] + dx
        ny = fantasma["y"] + dy
        if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
            if mapa[ny][nx] != 1:
                fantasma["x"], fantasma["y"] = nx, ny
    else:
        caminho = bfs((fantasma["x"], fantasma["y"]), (pac_x, pac_y))
        if len(caminho) > 1:
            fantasma["x"], fantasma["y"] = caminho[1]


# ================= DESENHAR =================
def desenhar():
    tela.fill(PRETO)

    for y in range(LINHAS):
        for x in range(COLUNAS):
            rect = (x * TAMANHO, y * TAMANHO, TAMANHO, TAMANHO)
            if mapa[y][x] == 1:
                pygame.draw.rect(tela, AZUL, rect)
            elif mapa[y][x] == 0:
                pygame.draw.circle(
                    tela, BRANCO, (x * TAMANHO + 12, y * TAMANHO + 12), 3
                )
            elif mapa[y][x] == 3:
                pygame.draw.circle(
                    tela, BRANCO, (x * TAMANHO + 12, y * TAMANHO + 12), 6
                )

    pygame.draw.circle(tela, AMARELO, (pac_x * TAMANHO + 12, pac_y * TAMANHO + 12), 10)

    cor = AZUL_FRACO if power else VERMELHO
    pygame.draw.circle(
        tela, cor, (fantasma["x"] * TAMANHO + 12, fantasma["y"] * TAMANHO + 12), 10
    )

    texto = font.render(f"Pontos: {pontuacao}  Vidas: {vidas}", True, BRANCO)
    tela.blit(texto, (10, 5))

    pygame.display.flip()


# ================= LOOP =================
while True:
    clock.tick(10)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                proxima_direcao = (-1, 0)
            if e.key == pygame.K_d:
                proxima_direcao = (1, 0)
            if e.key == pygame.K_w:
                proxima_direcao = (0, -1)
            if e.key == pygame.K_s:
                proxima_direcao = (0, 1)

    mover_pacman()
    mover_fantasma()

    # colisão
    if pac_x == fantasma["x"] and pac_y == fantasma["y"]:
        if power:
            pontuacao += 200 * (2**fantasmas_comidos)
            fantasmas_comidos += 1
            fantasma["x"], fantasma["y"] = 23, 28
        else:
            vidas -= 1
            pac_x, pac_y = 1, 1
            direcao = (0, 0)
            if vidas <= 0:
                tela.fill(PRETO)
                msg = font_big.render("GAME OVER", True, VERMELHO)
                tela.blit(msg, (LARGURA // 2 - 150, ALTURA // 2))
                pygame.display.flip()
                pygame.time.delay(000)
                pygame.quit()
                sys.exit()

    if power and pygame.time.get_ticks() - power_timer > 6000:
        power = False

    desenhar()
