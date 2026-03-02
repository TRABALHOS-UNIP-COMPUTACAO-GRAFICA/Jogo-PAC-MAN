import pygame
import sys

# Inicializa o pygame
pygame.init()

# Configurações
TAMANHO_BLOCO = 24
LINHAS = 30
COLUNAS = 25
LARGURA = COLUNAS * TAMANHO_BLOCO
ALTURA = LINHAS * TAMANHO_BLOCO

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
    [1]*25,
    [1]+[0]*23+[1],
    [1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,0,0,0,1],
    [1]+[0]*23+[1],
    [1,1]+[0]*21+[1,1],
   [0,1]+[0]*21+[1,0],
    [0,1]+[0]*21+[1,0],
    [0,1]+[0]*21+[1,0],
    [0,1]+[0]*21+[1,0],
[0,1]+[0]*21+[1,0],
[0,1]+[0]*21+[1,0],
[0,1]+[0]*21+[1,0],
[0,1]+[0]*21+[1,0],
    [1,1]+[0]*21+[1,1],
     [0,0,0]+[1,0]*9+[1,0,0,0],
     [0,0,0]+[1,0]*9+[1,0,0,0],
     [1,1]+[0]*21+[1,1],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [0,1]+[0]*21+[1,0],
     [1,1]+[0]*21+[1,1],
    [1]+[0]*23+[1],
    [1]+[0]*23+[1],
    [1]+[0]*23+[1],
    [1]*25
]

# Pac-Man
pac_x = 1
pac_y = 1
direcao = (0, 0)
pontuacao = 0

clock = pygame.time.Clock()
ultimo = pygame.time.get_ticks()
atraso = 2000
def desenhar():
    tela.fill(PRETO)

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = coluna * TAMANHO_BLOCO
            y = linha * TAMANHO_BLOCO

            if mapa[linha][coluna] == 1:
                pygame.draw.rect(tela, AZUL, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
            elif mapa[linha][coluna] == 0 and coluna !=0 and coluna != COLUNAS-1 :
                pygame.draw.circle(tela, BRANCO, 
                                   (x + TAMANHO_BLOCO//2, y + TAMANHO_BLOCO//2), 4)

    # Desenha Pac-Man
    pygame.draw.circle(tela, AMARELO,
                       (pac_x * TAMANHO_BLOCO + TAMANHO_BLOCO//2,
                        pac_y * TAMANHO_BLOCO + TAMANHO_BLOCO//2),
                       TAMANHO_BLOCO//2 - 2)

    pygame.display.flip()
def mover():
    global pac_x, pac_y, pontuacao

    novo_x = (pac_x + direcao[0]) % COLUNAS
    novo_y = (pac_y + direcao[1]) % LINHAS

    if mapa[novo_y][novo_x] != 1:
        pac_x = novo_x
        pac_y = novo_y

        if mapa[pac_y][pac_x] == 0:
            mapa[pac_y][pac_x] = 2
            pontuacao += 10
while True:
    clock.tick(60) 

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
    mover()
    desenhar() 
    text_surface= font.render("Pontuação: " + str(pontuacao), True, BRANCO)
  
    tela.blit(text_surface, (10, ALTURA+15))

    pygame.display.update()
    pygame.display.update()
