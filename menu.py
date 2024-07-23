import pygame
import sys
from main import Juego  # Asegúrate de que la importación sea correcta

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((1600, 400))
pygame.display.set_caption("Menú")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar fuentes
font = pygame.font.Font(None, 74)

# Cargar imágenes para botones
normal_button_image = pygame.image.load('img/normal.png')
dificil_button_image = pygame.image.load('img/dificil.png')
normal_button_image = pygame.transform.scale(normal_button_image, (200, 100))
dificil_button_image = pygame.transform.scale(dificil_button_image, (200, 100))

# Configurar botones
normal_button_rect = normal_button_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
dificil_button_rect = dificil_button_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 90))

# Función para dibujar la pantalla del menú
def dibujar_menu():
    screen.fill(WHITE)
    texto = font.render('Seleccione la dificultad', True, BLACK)
    screen.blit(texto, (screen.get_width() // 2 - texto.get_width() // 2, 50))
    screen.blit(normal_button_image, normal_button_rect.topleft)
    screen.blit(dificil_button_image,dificil_button_rect.topleft)

# Bucle principal del menú
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if normal_button_rect.collidepoint(event.pos):
                juego = Juego('normal')  # Iniciar el juego en modo normal
                juego.run_game()  # Llama al método run_game para iniciar el juego
            elif dificil_button_rect.collidepoint(event.pos):
                juego = Juego('dificil')  # Iniciar el juego en modo difícil
                juego.run_game()  # Llama al método run_game para iniciar el juego

    dibujar_menu()
    pygame.display.flip()
