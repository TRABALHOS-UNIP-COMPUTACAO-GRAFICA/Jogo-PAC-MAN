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
tempo_fantasma = 0
velocidade_fantasma = 300
iniciado = False
tempo_inicio_fantasma = pygame.time.get_ticks()
delay_perseguicao = 3000  # 3 segundos

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
mapa = [
    [1] * 25,
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
    [1] * 25,
]

mapa_original = [linha[:] for linha in mapa]

# ================= ESTADO =================
pac_x, pac_y = 12, 17
direcao = (0, 0)
pontuacao = 0
vidas = 3
power = False
power_timer = 0
game_over = False
vitoria = False

fantasma = {"x": 12, "y": 12}


# ================= FUNÇÕES =================
def eh_parede(valor):
    return valor in (1, 4, 9)


def neighbor(y, x):
    if 0 <= y < LINHAS and 0 <= x < COLUNAS:
        return mapa[y][x] in (0, 2)
    return False


def bfs(inicio, fim):
    fila = deque([inicio])
    visitado = {inicio: None}

    while fila:
        atual = fila.popleft()
        if atual == fim:
            caminho = []
            while atual is not None:
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


def reset_posicoes():
    global pac_x, pac_y, direcao
    pac_x, pac_y = 12, 17
    direcao = (0, 0)
    fantasma["x"], fantasma["y"] = 12, 12
    global tempo_inicio_fantasma
    tempo_inicio_fantasma = pygame.time.get_ticks()


def mover_fantasma():
    global vidas, pontuacao, power, game_over, tempo_fantasma
    agora = pygame.time.get_ticks()

    # delay de 3s antes do fantasma começar a perseguir
    if agora - tempo_inicio_fantasma < delay_perseguicao:
        return

    if agora - tempo_fantasma < velocidade_fantasma:
        return
    tempo_fantasma = agora
    if power:
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nx, ny = fantasma["x"] + dx, fantasma["y"] + dy
        if 0 <= nx < COLUNAS and 0 <= ny < LINHAS:
            if not eh_parede(mapa[ny][nx]):
                fantasma["x"], fantasma["y"] = nx, ny
    else:
        caminho = bfs((fantasma["x"], fantasma["y"]), (pac_x, pac_y))
        if len(caminho) > 1:
            fantasma["x"], fantasma["y"] = caminho[1]

    if fantasma["x"] == pac_x and fantasma["y"] == pac_y:
        if power:
            pontuacao += 200
            fantasma["x"], fantasma["y"] = 12, 12
        else:
            vidas -= 1
            if vidas <= 0:
                game_over = True
            else:
                reset_posicoes()


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

    # ================= EVENTOS =================
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:

            # Iniciar jogo
            if e.key == pygame.K_SPACE and not iniciado:
                iniciado = True

            # Reiniciar
            elif e.key == pygame.K_r:
                resetar()
                iniciado = False
            elif e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Movimento
            elif iniciado and not game_over and not vitoria:

                if e.key == pygame.K_LEFT:
                    direcao = (-1, 0)

                elif e.key == pygame.K_RIGHT:
                    direcao = (1, 0)

                elif e.key == pygame.K_UP:
                    direcao = (0, -1)

                elif e.key == pygame.K_DOWN:
                    direcao = (0, 1)

    # ================= LÓGICA DO JOGO =================
    if iniciado and not game_over and not vitoria:

        mover()
        mover_fantasma()

        if power and pygame.time.get_ticks() - power_timer > 4000:
            power = False

        if not any(0 in linha or 3 in linha for linha in mapa):
            vitoria = True

    # ================= DESENHO =================
    tela.fill((10, 10, 25))

    # ===== Tela inicial =====
    if not iniciado:
        titulo = pygame.font.SysFont("Arial", 50, bold=True)
        subtitulo = pygame.font.SysFont("Arial", 25)

        tela.blit(
            titulo.render("PAC-MAN", True, AMARELO),
            (LARGURA // 2 - 120, ALTURA // 2 - 80),
        )

        tela.blit(
            subtitulo.render(
                "Pressione ESPAÇO para iniciar ou ESC para sair", True, BRANCO
            ),
            (LARGURA // 2 - 195, ALTURA // 2),
        )

        pygame.display.flip()
        continue

    # ================= MAPA =================
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):

            x = coluna * TAMANHO_BLOCO
            y = linha * TAMANHO_BLOCO

            if mapa[linha][coluna] == 1:

                cima = neighbor(linha - 1, coluna)
                baixo = neighbor(linha + 1, coluna)
                esquerda = neighbor(linha, coluna - 1)
                direita = neighbor(linha, coluna + 1)

                raio = 10

                pygame.draw.rect(
                    tela,
                    (0, 0, 180),
                    (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO),
                    border_top_left_radius=raio if (cima and esquerda) else 0,
                    border_top_right_radius=raio if (cima and direita) else 0,
                    border_bottom_left_radius=raio if (baixo and esquerda) else 0,
                    border_bottom_right_radius=raio if (baixo and direita) else 0,
                )

            elif mapa[linha][coluna] == 0:
                pygame.draw.circle(
                    tela,
                    (255, 255, 200),
                    (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2),
                    3,
                )

            elif mapa[linha][coluna] == 3:
                pygame.draw.circle(
                    tela,
                    (255, 255, 255),
                    (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2),
                    6,
                )

    # ================= PACMAN =================
    pygame.draw.circle(
        tela,
        AMARELO,
        (pac_x * TAMANHO_BLOCO + 12, pac_y * TAMANHO_BLOCO + 12),
        10,
    )

    # ================= FANTASMA =================
    cor = (100, 100, 255) if power else (255, 60, 60)

    pygame.draw.circle(
        tela,
        cor,
        (fantasma["x"] * TAMANHO_BLOCO + 12, fantasma["y"] * TAMANHO_BLOCO + 12),
        10,
    )

    # ================= HUD =================
    pygame.draw.rect(tela, (20, 20, 40), (0, ALTURA, LARGURA, 60))

    texto = font.render(f"Pontuação: {pontuacao}", True, BRANCO)
    tela.blit(texto, (20, ALTURA + 20))

    for i in range(vidas):
        pygame.draw.circle(
            tela,
            AMARELO,
            (LARGURA - 120 + i * 30, ALTURA + 30),
            10,
        )

    # ================= MENSAGENS =================
    if game_over:

        # Fundo escurecido transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        fonte_grande = pygame.font.SysFont("Arial", 60, bold=True)
        fonte_pequena = pygame.font.SysFont("Arial", 25)

        # Efeito piscando
        if (pygame.time.get_ticks() // 500) % 2 == 0:

            texto_principal = fonte_grande.render("GAME OVER", True, VERMELHO)
            sombra = fonte_grande.render("GAME OVER", True, (80, 0, 0))

            rect = texto_principal.get_rect(center=(LARGURA // 2, ALTURA // 2 - 30))

            # Sombra
            tela.blit(sombra, (rect.x + 4, rect.y + 4))
            tela.blit(texto_principal, rect)

        texto_secundario = fonte_pequena.render(
            "Pressione R para reiniciar ou ESC para sair", True, BRANCO
        )

        rect2 = texto_secundario.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30))
        tela.blit(texto_secundario, rect2)

    if vitoria:

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

    pygame.display.flip()
