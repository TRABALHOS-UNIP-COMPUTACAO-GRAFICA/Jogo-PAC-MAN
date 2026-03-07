import pygame
import sys
import random
from collections import deque

from sqlalchemy import case

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
vitoria = False
tela = pygame.display.set_mode((LARGURA,800))
pygame.display.set_caption("Pac-Man")
font = pygame.font.SysFont("Arial", 20)
tempo_fantasma = 0 
game_over = False
# Cores
frutas = 297
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
# Mapa (1 = parede, 0 = caminho com ponto)

mapa_original = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 0
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1], # 1
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 2
    [1, 0, 1, 2, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 1, 2, 2, 2, 1, 0, 1, 2, 1, 0, 1], # 3
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 4
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 5
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1], # 6
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], # 7
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 8
    [2, 2, 2, 2, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 2, 2, 2, 2], # 2
    [2, 2, 2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2, 2, 2], # 10
    [2, 2, 2, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 2, 2, 2], # 11
    [2, 2, 2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2, 2, 2], # 12
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 4, 4, 4, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 13
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0], # 14
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0], # 15
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 16
    [2, 2, 2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2, 2, 2], # 17
    [2, 2, 2, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 2, 2, 2], # 18
    [2, 2, 2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 2, 2, 2, 2], # 12
    [2, 2, 2, 2, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 2, 2, 2, 2], # 20
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1], # 21
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], # 22
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1], # 23
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 24
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 25
    [1, 0, 1, 2, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 1, 2, 2, 2, 1, 0, 1, 2, 1, 0, 1], # 3
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], # 27
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1], # 28
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 22
]
mapa = mapa_original
# Pac-Man
pac_x = 12
pac_y = 17
direcao = (0, 0)
pontuacao = 0
vidas = 3
power = False
power_timer = 0
fantasmas_comidos = 0
tempo_animacao = 0
frame_boca = 0  # 0 = fechada, 1 = entreaberta, 2 = aberta
velocidade_animacao = 150 # milissegundos
# ================= FANTASMA =================
fantasma = {"x": 10, "y": 15}
# ================= POWER PELLETS =================
tempo_inicio_fantasma = pygame.time.get_ticks()
delay_perseguicao = 300  # 3 segundos
velocidade_fantasma = 150


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
                if mapa[ny][nx] != 1 and mapa[ny][nx] != 4 and (nx, ny) not in visitado:
                    fila.append((nx, ny))
                    visitado[(nx, ny)] = atual
    return []
# ================= MOVIMENTO FANTASMA =================
def mover_fantasma():
    global vidas, pontuacao, power, game_over,mapa, tempo_fantasma
    if agora - tempo_inicio_fantasma < delay_perseguicao:
        return

    if agora - tempo_fantasma < velocidade_fantasma:
        return
    tempo_fantasma = agora
    if fantasma["x"] == 10 and fantasma["y"] ==15:
                mapa[13][13]=2
                mapa[13][11]=2
                mapa[13][12]=2
    elif fantasma["x"] == 14 and fantasma["y"] in(11,12,13):
                mapa[13][13]=4
                mapa[13][11]=4
                mapa[13][12]=4        

    if power== True:
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nx = fantasma["x"] + dx
        ny = fantasma["y"] + dy
        if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
            if mapa[ny][nx] != 4 and mapa[ny][nx] != 1:
                fantasma["x"], fantasma["y"] = nx, ny
    else:

        caminho = bfs((fantasma["x"], fantasma["y"]), (pac_x, pac_y))
        if len(caminho) > 1:
            fantasma["x"], fantasma["y"] = caminho[1]

    # Colisão
    if fantasma["x"] == pac_x and fantasma["y"] == pac_y:
        if power == True:
            pontuacao += 200
            fantasma["x"], fantasma["y"] = 10, 15
            power = False
        else:
            vidas -= 1
            if vidas <= 0:
                game_over = True
            else:
                reset_posicoes()
def neighbor(x, y):
    if LINHAS > x >= 0 and  COLUNAS > y >= 0:
        if mapa[x][y] == 0 or mapa[x][y] == 2:
            return True
        return False
    return False
    
def desenhar():
    tela.fill(PRETO)
    global frame_boca, tempo_animacao
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = coluna * TAMANHO_BLOCO
            y = linha * TAMANHO_BLOCO

            match mapa[linha][coluna]:
                case 1:
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
                    # pygame.draw.circle(tela, PRETO, (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 2)
                case 0  :
                    pygame.draw.circle(tela, BRANCO, 
                                    (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 4)
                case 3:
                    pygame.draw.circle(
                        tela, BRANCO, (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 6
                    )
                case 4:
                    pygame.draw.rect(tela, [128,128,128], (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))

    # Desenha Pac-Man
    pygame.draw.circle(tela, AMARELO,
                       (pac_x * TAMANHO_BLOCO + TAMANHO_BLOCO//2,
                        pac_y * TAMANHO_BLOCO + TAMANHO_BLOCO//2),
                       TAMANHO_BLOCO//2 - 2,
                       draw_top_left= True,
                       draw_top_right= True,
                       draw_bottom_left= True,
                       draw_bottom_right= True)
    if power ==True:
        cor = AZUL_FRACO 
    else:
        cor =VERMELHO
    pygame.draw.circle(
    tela, cor, (fantasma["x"] * TAMANHO_BLOCO + 12, fantasma["y"] * TAMANHO_BLOCO + 12), 10)
    for i in range(vidas):
        x_vida = 500 + (i * 30) # Espaçamento entre os ícones
        y_vida = ALTURA + 25 # Centralizado no painel de 50px
        
        # Desenha um pequeno Pac-Man como ícone de vida
        pygame.draw.circle(tela, AMARELO, (x_vida, y_vida), 10)

    pygame.display.flip()
# ================= MOVIMENTO PACMAN =================
def reset_posicoes():
    global pac_x, pac_y, direcao
    pac_x, pac_y = 12, 17
    direcao = (0, 0)
    fantasma["x"], fantasma["y"] = 10, 15


def resetar():
    global mapa, pontuacao, vidas, power, game_over, vitoria
    mapa = mapa_original
    pontuacao = 0
    vidas = 3
    power = False
    game_over = False
    vitoria = False
    reset_posicoes()


def mover_pacman():
    global fantasmas_comidos, direcao, direcao, pac_x, pac_y, pontuacao, power, power_timer ,frutas,velocidade_fantasma,delay_perseguicao

    # tenta virar
    nx = (pac_x + direcao[0]) % COLUNAS
    ny = (pac_y + direcao[1]) % LINHAS

    if mapa[ny][nx] != 1 :
        
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
                frutas -= 1
                # velocidade_fantasma -=20
                # delay_perseguicao -=20
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
    milissegundos = pygame.time.get_ticks() 
    segundos2 = 0
    segundos = milissegundos // 1000
    if  segundos == 4 :

        mapa[13][13]=0
        mapa[13][11]=0
        mapa[13][12]=0

    elif segundos == 6 :
        mapa[13][13]=4
        mapa[13][11]=4
        mapa[13][12]=4
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            match evento.key:
                case pygame.K_a|pygame.K_LEFT:
                    direcao = (-1, 0)
                case pygame.K_d|pygame.K_RIGHT:
                    direcao = (1, 0)
                case pygame.K_w|pygame.K_UP:
                    direcao = (0, -1)
                case pygame.K_s|pygame.K_DOWN:
                    direcao = (0, 1)
                case pygame.K_r :
                    if game_over == True or vitoria == True:
                        resetar()
    if power and pygame.time.get_ticks() - power_timer > 4000:
            power = False
    if agora - ultimo > atraso:
        ultimo = agora
    if frutas == 0 :
        vitoria = True
    if game_over == False and vitoria ==False:
        mover_pacman()
        
        mover_fantasma()
        desenhar() 
    if game_over == True:
        text_surface = font.render("Game Over! Press R to Restart", True, BRANCO)
        tela.blit(text_surface, (LARGURA//2 - text_surface.get_width()//2, ALTURA//2))
    if not any(0 in linha or 3 in linha for linha in mapa):
            vitoria = True
    if vitoria == True:

        # Fundo escurecido transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        fonte_grande = pygame.font.SysFont("Arial", 60, bold=True)
        fonte_pequena = pygame.font.SysFont("Arial", 25)

        # Efeito piscando dourado
        if (pygame.time.get_ticks() // 400) % 2 == 0:

            texto_principal = fonte_grande.render("VOCÊ VENCEU!", True, (255, 215, 0))
            sombra = fonte_grande.render("VOCÊ VENCEU!", True, (120, 90, 0))

            rect = texto_principal.get_rect(center=(LARGURA // 2, ALTURA // 2 - 30))

            # sombra
            tela.blit(sombra, (rect.x + 4, rect.y + 4))
            tela.blit(texto_principal, rect)

        texto_secundario = fonte_pequena.render(
            "Pressione R para jogar novamente ou ESC para sair",
            True,
            BRANCO,
        )

        rect2 = texto_secundario.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30))
        tela.blit(texto_secundario, rect2)
    text_surface= font.render("Pontuação: " + str(pontuacao), True, BRANCO)
  
    tela.blit(text_surface, (10, ALTURA+15))

    pygame.display.update()
