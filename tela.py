import pygame
import sys
import random
from collections import deque

pygame.init()

# ================= CONFIG =================
TAMANHO_BLOCO = 24
LINHAS = 30
COLUNAS = 25
LARGURA = COLUNAS * TAMANHO_BLOCO
ALTURA = LINHAS * TAMANHO_BLOCO

tela = pygame.display.set_mode((LARGURA, ALTURA + 60))
pygame.display.set_caption("Pac-Man")
font = pygame.font.SysFont("Arial", 20)

# ================= CORES =================
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# ================= MAPA =================
# ================= MAPA =================
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 9, 1, 0, 1, 9, 9, 9, 1, 0, 1, 0, 1, 9, 9, 9, 1, 0, 1, 9, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [9, 9, 9, 9, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 4, 4, 4, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9],
    [9, 9, 9, 9, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 9, 9, 9, 9],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 9, 1, 0, 1, 9, 9, 9, 1, 0, 1, 0, 1, 9, 9, 9, 1, 0, 1, 9, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

mapa_original = [linha[:] for linha in mapa]

# ================= ESTADO DO JOGO =================
pac_x, pac_y = 12, 17
direcao = (0, 0)
pontuacao = 0
vidas = 3
power = False
power_timer = 0
game_over = False
vitoria = False

fantasma = {"x": 23, "y": 28}


# ================= FUNÇÕES AUXILIARES =================
def eh_parede(valor):
    return valor in (1, 4, 9)


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
                if not eh_parede(mapa[ny][nx]) and (nx, ny) not in visitado:
                    fila.append((nx, ny))
                    visitado[(nx, ny)] = atual
    return []


# ================= MOVIMENTO PAC =================
def mover():
    global pac_x, pac_y, pontuacao, power, power_timer

    nx = (pac_x + direcao[0]) % COLUNAS
    ny = (pac_y + direcao[1]) % LINHAS

    if not eh_parede(mapa[ny][nx]):
        pac_x, pac_y = nx, ny

        if mapa[ny][nx] == 0:
            mapa[ny][nx] = 2
            pontuacao += 10

        elif mapa[ny][nx] == 3:
            mapa[ny][nx] = 2
            pontuacao += 50
            power = True
            power_timer = pygame.time.get_ticks()


# ================= MOVIMENTO FANTASMA =================
def mover_fantasma():
    global vidas, pontuacao, power, game_over

    if power:
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nx = fantasma["x"] + dx
        ny = fantasma["y"] + dy
        if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
            if not eh_parede(mapa[ny][nx]):
                fantasma["x"], fantasma["y"] = nx, ny
    else:
        caminho = bfs((fantasma["x"], fantasma["y"]), (pac_x, pac_y))
        if len(caminho) > 1:
            fantasma["x"], fantasma["y"] = caminho[1]

    # Colisão
    if fantasma["x"] == pac_x and fantasma["y"] == pac_y:
        if power:
            pontuacao += 200
            fantasma["x"], fantasma["y"] = 23, 28
        else:
            vidas -= 1
            power = False
            if vidas <= 0:
                game_over = True
            else:
                reset_posicoes()


# ================= RESET POSIÇÕES =================
def reset_posicoes():
    global pac_x, pac_y, direcao
    pac_x, pac_y = 12, 17
    direcao = (0, 0)
    fantasma["x"], fantasma["y"] = 23, 28


# ================= RESET TOTAL =================
def resetar():
    global mapa, pontuacao, vidas, power, game_over, vitoria
    mapa = [linha[:] for linha in mapa_original]
    pontuacao = 0
    vidas = 3
    power = False
    game_over = False
    vitoria = False
    reset_posicoes()


# ================= LOOP =================
clock = pygame.time.Clock()

while True:
    clock.tick(10)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                direcao = (-1, 0)
            if e.key == pygame.K_d:
                direcao = (1, 0)
            if e.key == pygame.K_w:
                direcao = (0, -1)
            if e.key == pygame.K_s:
                direcao = (0, 1)
            if e.key == pygame.K_r:
                resetar()

    if not game_over and not vitoria:
        mover()
        mover_fantasma()

        if power and pygame.time.get_ticks() - power_timer > 4000:
            power = False

        # Vitória
        if not any(0 in linha or 3 in linha for linha in mapa):
            vitoria = True

    # ================= DESENHO =================
    tela.fill(PRETO)

    for y in range(LINHAS):
        for x in range(COLUNAS):
            if eh_parede(mapa[y][x]):
                pygame.draw.rect(
                    tela,
                    AZUL,
                    (
                        x * TAMANHO_BLOCO,
                        y * TAMANHO_BLOCO,
                        TAMANHO_BLOCO,
                        TAMANHO_BLOCO,
                    ),
                )
            elif mapa[y][x] == 0:
                pygame.draw.circle(
                    tela, BRANCO, (x * TAMANHO_BLOCO + 12, y * TAMANHO_BLOCO + 12), 3
                )
            elif mapa[y][x] == 3:
                pygame.draw.circle(
                    tela, BRANCO, (x * TAMANHO_BLOCO + 12, y * TAMANHO_BLOCO + 12), 6
                )

    pygame.draw.circle(
        tela, AMARELO, (pac_x * TAMANHO_BLOCO + 12, pac_y * TAMANHO_BLOCO + 12), 10
    )

    cor_fantasma = (100, 100, 255) if power else VERMELHO
    pygame.draw.circle(
        tela,
        cor_fantasma,
        (fantasma["x"] * TAMANHO_BLOCO + 12, fantasma["y"] * TAMANHO_BLOCO + 12),
        10,
    )

    for i in range(vidas):
        pygame.draw.circle(tela, AMARELO, (20 + i * 30, ALTURA + 30), 10)

    texto = font.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto, (10, ALTURA + 5))

    if game_over:
        over = font.render("GAME OVER - Pressione R", True, VERMELHO)
        tela.blit(over, (LARGURA // 2 - 100, ALTURA // 2))

    if vitoria:
        win = font.render("VOCÊ VENCEU! - R para reiniciar", True, AMARELO)
        tela.blit(win, (LARGURA // 2 - 150, ALTURA // 2))

    pygame.display.flip()