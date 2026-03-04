class Player:
    def __init__(self, x, y):
        self.x = 12
        self.y = 17
        self.vidas = 3
        self.pontuacao = 0
        
    def mover_pacman(self,fantasmas_comidos, direcao, pac_x, pac_y, power, power_timer,linhas,colunas,mapa):
     

    # tenta virar
        nx = (self.x + direcao[0]) % colunas
        ny = (self.y + direcao[1]) % linhas

        if mapa[ny][nx] != 1 :
            
                pac_x = nx
                pac_y = ny

                if mapa[pac_y][pac_x] == 0:
                    mapa[pac_y][pac_x] = 2
                    self.pontuacao += 10
        if 0 <= nx < colunas and 0 <= ny < linhas:
            if mapa[ny][nx] != 1:
                pac_x, pac_y = nx, ny

                if mapa[ny][nx] == 0:
                    mapa[ny][nx] = 2
                    self.pontuacao += 10

                if mapa[ny][nx] == 3:
                    mapa[ny][nx] = 2
                    self.pontuacao += 50
                    power = True
                    fantasmas_comidos = 0