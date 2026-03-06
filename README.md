🟡 Pac-Man em Python

Projeto desenvolvido para a disciplina de Computação Gráfica, que apresenta uma réplica do clássico jogo Pac-Man, utilizando Python e a biblioteca Pygame.

O objetivo do projeto é aplicar conceitos estudados em aula, como primitivas gráficas, lógica de movimentação, detecção de colisão e inteligência artificial básica para os fantasmas.

⸻

🎮 Sobre o Projeto

Este projeto implementa uma versão jogável do Pac-Man com:
	•	Labirinto inspirado no jogo clássico
	•	Sistema de pontuação
	•	Sistema de vidas
	•	Power Pellet (modo de poder)
	•	Inteligência artificial para os fantasmas
	•	Tela inicial
	•	Tela de vitória
	•	Tela de Game Over
	•	Reinício do jogo

O jogo foi desenvolvido utilizando primitivas gráficas do Pygame, como:
	•	pygame.draw.rect()
	•	pygame.draw.circle()

Essas primitivas são usadas para desenhar o labirinto, o Pac-Man, os fantasmas e os itens do jogo.

⸻

🧠 Inteligência Artificial dos Fantasmas

Os fantasmas utilizam um algoritmo de busca baseado em BFS (Breadth-First Search) para encontrar o menor caminho até o Pac-Man.

Cada fantasma possui um comportamento inspirado no jogo original:

🔴 Blinky
	•	Persegue diretamente o Pac-Man.

🌸 Pinky
	•	Tenta prever a posição do Pac-Man alguns blocos à frente.

🔵 Inky
	•	Calcula um alvo baseado na direção do Pac-Man.

🟠 Clyde
	•	Persegue o Pac-Man quando está longe.
	•	Quando está perto, foge para um canto do mapa.

Quando o Pac-Man come uma Power Pellet, os fantasmas entram em modo de fuga e se movem aleatoriamente.

⸻

🗺️ Estrutura do Mapa

O mapa do jogo é representado por uma matriz, onde cada número representa um tipo de elemento: