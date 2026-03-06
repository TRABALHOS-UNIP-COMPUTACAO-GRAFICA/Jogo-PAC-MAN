🟡 Pac-Man em Python

Este projeto apresenta uma réplica do jogo Pac-Man, desenvolvida utilizando Python e a biblioteca Pygame, aplicando conceitos estudados em Computação Gráfica.
O jogo utiliza primitivas gráficas para desenhar os elementos do cenário e personagens, além de implementar lógica de movimentação, inteligência artificial para fantasmas e sistema de pontuação.

👥 Integrantes do Grupo
Nome
RA
Sydhiney Silva
G75EJI5
Eduardo Theodoro
R153FJ3
Ariane Veras
R197123
Victor Donadi
G593IC1

🎮 Demonstração do jogo

No jogo o jogador controla o Pac-Man, que deve percorrer o labirinto coletando pontos enquanto evita os fantasmas.

Funcionalidades principais:
	•	Labirinto baseado no mapa clássico
	•	Sistema de pontuação
	•	Sistema de vidas
	•	Power pellets (modo de poder)
	•	Inteligência artificial para os fantasmas
	•	Tela inicial
	•	Tela de vitória
	•	Tela de Game Over
	•	Reinício de partida

🧠 Inteligência Artificial dos Fantasmas

Os fantasmas utilizam busca em grafos para perseguir o jogador.

Algoritmo utilizado:
	•	Breadth First Search (BFS) para encontrar o menor caminho até o Pac-Man.

Cada fantasma possui comportamento inspirado no jogo original:

Fantasma
Cor
Comportamento
Blinky
Vermelho
Persegue diretamente o Pac-Man
Pinky
Rosa
Tenta prever a posição futura do Pac-Man
Inky
Ciano
Persegue com estratégia intermediária
Clyde
Laranja
Alterna entre perseguir e fugir

🗺️ Estrutura do Mapa

O mapa do jogo é representado por uma matriz onde cada número representa um tipo de elemento.

Valor
Significado
0
Caminho com ponto
1
Parede
2
Caminho já percorrido
3
Power Pellet
4
Porta da casa dos fantasmas
9
Área bloqueada do mapa

