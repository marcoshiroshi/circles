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
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 180


rainbow_colors = [
    (148, 0, 211),  # Violeta
    (75, 0, 130),  # Índigo
    (0, 0, 255),  # Azul
    (0, 255, 0),  # Verde
    (255, 255, 0),  # Amarelo
    (255, 127, 0),  # Laranja
    (255, 0, 0)  # Vermelho
]


# Função para gerar cores intermediárias
def interpolate_colors(color1, color2, steps):
    step_r = (color2[0] - color1[0]) / steps
    step_g = (color2[1] - color1[1]) / steps
    step_b = (color2[2] - color1[2]) / steps
    return [
        (
            int(color1[0] + step_r * i),
            int(color1[1] + step_g * i),
            int(color1[2] + step_b * i)
        )
        for i in range(steps)
    ]


smooth_colors = []
steps_per_color = 20  # Ajuste este valor para mais ou menos suavidade

current_color_index = 0

for i in range(len(rainbow_colors) - 1):
    smooth_colors.extend(interpolate_colors(rainbow_colors[i], rainbow_colors[i + 1], steps_per_color))

# Adicione a última cor manualmente
smooth_colors.append(rainbow_colors[-1])

# Inicialização da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circunferência com Bola")

# Fonte para o contador de colisões
font = pygame.font.Font(None, 36)

# Inicialização da música
# pygame.mixer.music.load("megalovania.mp3")  # Substitua "exemplo_musica.mp3" pelo caminho do seu arquivo de música
pygame.mixer.music.load("tokyo_drift.mp3")  # Substitua "exemplo_musica.mp3" pelo caminho do seu arquivo de música

music_playing = False
collision_timer = 0
collision_duration = 200  # Duração da reprodução da música em milissegundos
pause_time = 0
fadeout_duration = 100


# Função para verificar colisão da bola com a circunferência
def check_collision(ball_pos, center, radius):
    distance = math.sqrt((ball_pos[0] - center[0]) ** 2 + (ball_pos[1] - center[1]) ** 2)
    return distance >= radius


# Função para gerar direção aleatória
def generate_random_direction(ball_pos, center):
    if ball_pos != center:
        # Gerar um vetor apontando para dentro da circunferência
        direction_vector = [center[0] - ball_pos[0], center[1] - ball_pos[1]]
        # Normalizar o vetor para garantir que tenha comprimento 1
        length = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
        direction_vector[0] /= length
        direction_vector[1] /= length
        # Adicionar uma pequena perturbação aleatória
        direction_vector[0] += random.uniform(-0.2, 0.2)
        direction_vector[1] += random.uniform(-0.2, 0.2)
        return direction_vector
    else:
        return random.uniform(-1, 1), random.uniform(-1, 1)

# Inicialização da posição e velocidade da bola
ball_pos = list(CENTER)
ball_speed = list(generate_random_direction(CENTER, CENTER))

# Contador de colisões
collision_count = 0

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)

    # Desenhar circunferência
    pygame.draw.circle(screen, smooth_colors[current_color_index], CENTER, RADIUS, 5)

    # Desenhar bola
    pygame.draw.circle(screen, WHITE, [int(pos) for pos in ball_pos], 10)

    # Atualizar posição da bola
    ball_pos[0] += ball_speed[0] * pygame.time.get_ticks() / 5000  # Aumentando a velocidade
    ball_pos[1] += ball_speed[1] * pygame.time.get_ticks() / 5000

    # ball_pos[0] += ball_speed[0] * 3  # Aumentando a velocidade
    # ball_pos[1] += ball_speed[1] * 3


    # Verificar colisão com a circunferência
    if check_collision(ball_pos, CENTER, RADIUS - 10):  # 10 é o raio da bola
        current_color_index = (current_color_index + 1) % len(smooth_colors)
        pygame.draw.circle(screen, smooth_colors[current_color_index], CENTER, RADIUS, 5)

        # Repelir bola para uma direção aleatória
        ball_speed = list(generate_random_direction(ball_pos, CENTER))
        collision_count += 1

        # Reproduzir música por um segundo
        if not music_playing:
            pygame.mixer.music.play()
            music_playing = True
            collision_timer = pygame.time.get_ticks()
        else:
            pygame.mixer.music.unpause()
            collision_timer = pygame.time.get_ticks()

    # Verificar se o tempo de colisão decorreu
    if music_playing and pygame.time.get_ticks() - collision_timer >= collision_duration:
        # pygame.mixer.music.fadeout(fadeout_duration)
        pygame.mixer.music.pause()
        pause_time = pygame.mixer.music.get_pos()
        # music_playing = True

    # Desenhar contador de colisões
    text = font.render("Colisões: " + str(collision_count), True, WHITE)
    screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 + RADIUS + 20))

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

