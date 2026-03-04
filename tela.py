import pygame
import sys
import random
from collections import deque

# Inicializa o pygame
pygame.init()

# Configurações
TAMANHO_BLOCO = 24
LINHAS = 30
COLUNAS = 25
LARGURA = COLUNAS * TAMANHO_BLOCO
ALTURA = LINHAS * TAMANHO_BLOCO
VERMELHO = (255, 0, 0)
AZUL_FRACO = (100, 100, 255)

tela = pygame.display.set_mode((LARGURA,800))
pygame.display.set_caption("Pac-Man")
font = pygame.font.SysFont("Arial", 20)
# Cores
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
# Mapa (1 = parede, 0 = caminho com ponto)

mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 0
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1], # 1
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 2
    [1, 0, 1, 9, 1, 0, 1, 9, 9, 9, 1, 0, 1, 0, 1, 9, 9, 9, 1, 0, 1, 9, 1, 0, 1], # 3
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 4
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 5
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1], # 6
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], # 7
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 8
    [9, 9, 9, 9, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 9, 9, 9, 9], # 9
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9], # 10
    [9, 9, 9, 9, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 9, 9, 9, 9], # 11
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9], # 12
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 4, 4, 4, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 13
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0], # 14
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 9, 9, 9, 9, 9, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0], # 15
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 16
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9], # 17
    [9, 9, 9, 9, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 9, 9, 9, 9], # 18
    [9, 9, 9, 9, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 9, 9, 9, 9], # 19
    [9, 9, 9, 9, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 9, 9, 9, 9], # 20
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 21
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], # 22
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1], # 23
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 24
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 25
    [1, 0, 1, 9, 1, 0, 1, 9, 9, 9, 1, 0, 1, 0, 1, 9, 9, 9, 1, 0, 1, 9, 1, 0, 1], # 3
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 27
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1], # 28
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 29
]
# Pac-Man
pac_x = 12
pac_y = 17
direcao = (0, 0)
pontuacao = 0
vidas = 3
power = False
power_timer = 0
fantasmas_comidos = 0
power = False
power_timer = 0
fantasmas_comidos = 0
# ================= FANTASMA =================
fantasma = {"x": 10, "y": 15}
# ================= POWER PELLETS =================


clock = pygame.time.Clock()
ultimo = pygame.time.get_ticks()
atraso = 2000

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
def neighbor(x, y):
    if LINHAS > x >= 0 and  COLUNAS > y >= 0:
        if mapa[x][y] == 0 or mapa[x][y] == 2:
            return True
        return False
    return False
    
def desenhar():
    tela.fill(PRETO)

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = coluna * TAMANHO_BLOCO
            y = linha * TAMANHO_BLOCO

            if mapa[linha][coluna] == 1:
                cima = neighbor(linha-1, coluna)
                baixo = neighbor(linha+1, coluna)
                esquerda = neighbor(linha, coluna-1)
                direita = neighbor(linha, coluna+1) 
                raio = 12
                cando_ce= raio if (cima and esquerda) else 0
                cando_cd= raio if  (cima and direita) else 0
                cando_be= raio if  (baixo and esquerda) else 0
                cando_bd= raio if  (baixo and direita) else 0

                pygame.draw.rect(tela, AZUL, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO),
                                 border_bottom_left_radius=cando_be,
                                 border_bottom_right_radius=cando_bd,
                                 border_top_left_radius=cando_ce,
                                 border_top_right_radius=cando_cd)
                # pygame.draw.circle(tela, PRETO, (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 9)
            elif mapa[linha][coluna] == 0  :
                pygame.draw.circle(tela, BRANCO, 
                                   (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 4)
            elif mapa[linha][coluna] == 3:
                pygame.draw.circle(
                    tela, BRANCO, (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 6
                )

    # Desenha Pac-Man
    pygame.draw.circle(tela, AMARELO,
                       (pac_x * TAMANHO_BLOCO + TAMANHO_BLOCO//2,
                        pac_y * TAMANHO_BLOCO + TAMANHO_BLOCO//2),
                       TAMANHO_BLOCO//2 - 2,
                       draw_top_left= True,
                       draw_top_right= True,
                       draw_bottom_left= True,
                       draw_bottom_right= True)
    cor = AZUL_FRACO if power else VERMELHO
    pygame.draw.circle(
        tela, cor, (fantasma["x"] * TAMANHO_BLOCO + 12, fantasma["y"] * TAMANHO_BLOCO + 12), 10
    )
    for i in range(vidas):
        x_vida = 500 + (i * 30) # Espaçamento entre os ícones
        y_vida = ALTURA + 25 # Centralizado no painel de 50px
        
        # Desenha um pequeno Pac-Man como ícone de vida
        pygame.draw.circle(tela, AMARELO, (x_vida, y_vida), 10)

    pygame.display.flip()
# ================= MOVIMENTO PACMAN =================
def mover_pacman():
    global fantasmas_comidos, direcao, direcao, pac_x, pac_y, pontuacao, power, power_timer

    # tenta virar
    nx = (pac_x + direcao[0]) % COLUNAS
    ny = (pac_y + direcao[1]) % LINHAS

    if mapa[nx][ny] != 1:
        pac_x = nx
        pac_y = ny

        if mapa[pac_y][pac_x] == 0:
            mapa[pac_y][pac_x] = 2
            pontuacao += 10
    # move
   

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
while True:
    clock.tick(10) 

    agora = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                direcao = (-1, 0)
            if evento.key == pygame.K_d:
                direcao = (1, 0)
            if evento.key == pygame.K_w:
                direcao = (0, -1)
            if evento.key == pygame.K_s:
                direcao = (0, 1)
    if agora - ultimo > atraso:
        ultimo = agora
    mover_pacman()
    mover_fantasma()
    desenhar() 
    text_surface= font.render("Pontuação: " + str(pontuacao), True, BRANCO)
  
    tela.blit(text_surface, (10, ALTURA+15))

    pygame.display.update()
    pygame.display.update()
