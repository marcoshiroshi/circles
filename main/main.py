import pygame
import random
import math
import time

# Inicialização do Pygame
pygame.init()

# Definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configurações da tela
WIDTH, HEIGHT = 400, 800
#
# Inicialização da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("meu jogo")

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)

    # Limitar velocidade de atualização
    clock.tick(120)

    # Lidar com eventos
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            running = False

    # Atualizar a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()

