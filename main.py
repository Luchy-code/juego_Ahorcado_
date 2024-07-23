import pygame
import sys
import random
from juego import Ahorcado

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((1600, 400))
pygame.display.set_caption("Ahorcado")

# Colores
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar música
pygame.mixer.music.load('img/back.mp3')
pygame.mixer.music.play(-1)  # Reproducir en bucle

# Cargar imágenes y música
music_on_image = pygame.image.load('img/music_on.png')
music_off_image = pygame.image.load('img/music_off.png')
button_size = (40, 40)
music_on_image = pygame.transform.scale(music_on_image, button_size)
music_off_image = pygame.transform.scale(music_off_image, button_size)
button_image = music_on_image
button_rect = button_image.get_rect(topright=(screen.get_width() - 10, 10))
music_playing = True

# Cargar imagen del botón de reinicio
restart_button_image = pygame.image.load('img/restart.png')
restart_button_image = pygame.transform.scale(restart_button_image, (50, 50))
restart_button_rect = restart_button_image.get_rect()
restart_button_rect.center = (screen.get_width() - 50, screen.get_height() - 50)

# Cargar imagen del botón de continuar
continue_button_image = pygame.image.load('img/continue.png')
continue_button_image = pygame.transform.scale(continue_button_image, (50, 50))
continue_button_rect = continue_button_image.get_rect()
continue_button_rect.center = (screen.get_width() - 50, screen.get_height() - 50)

image1 = pygame.image.load('img/1.png')
image2 = pygame.image.load('img/2.png')
image3 = pygame.image.load('img/3.png')
image4 = pygame.image.load('img/4.png')
image5 = pygame.image.load('img/5.png')
image6 = pygame.image.load('img/6.png')
image7 = pygame.image.load('img/7.png')
ahorcado_images = [image1, image2, image3, image4, image5, image6, image7]
#assert len(ahorcado_images) == 7  # Cambia este número según el número de estados que tengas

vida_image = pygame.image.load('img/vida.png')
vida_image = pygame.transform.scale(vida_image, (22, 22))

def cargar_palabras(dificultad):
        if dificultad == 'normal':
            return ['huron', 'camaleon', 'cotorro', 'bulldog', 'elefante', 'jirafa', 'guacamaya'] #
        elif dificultad == 'dificil':
            return ['quijotesco', 'paralelepipedo', 'inconmensurable', 'desoxirribonucleico', 'otorrinolaringologo', 'hipopotomonstrosesquipedaliofobia', 'electroencefalografista']

def mostrar_mensaje(mensaje, color, duracion=3):
    font = pygame.font.Font(None, 74)
    texto = font.render(mensaje, True, color)
    texto_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.wait(duracion * 500)

class Juego:
    def __init__(self, dificultad):
        self.ahorcado_estado = 0  # Estado actual del ahorcado (0-6)
        self.dificultad = dificultad
        self.palabras = cargar_palabras(dificultad)
        self.ahorcado_images = ahorcado_images
        self.juego = Ahorcado(self.palabras, self.ahorcado_images)
        self.run_game()

    def reiniciar_juego(self):
        # Resetea el juego completamente
        self.juego.reiniciar_juego()

#lunes 18-20 y miercoles 18-22

    def nueva_ronda(self):
        if self.juego.juego_ganado():
            self.juego.sumar_punto()
        if self.juego.juego_perdido():
            self.juego.sumar_perdidas()

        self.juego.nueva_ronda()


        # Elige una nueva palabra si no hay ninguna actual
        if self.juego.obtener_palabra() is None or '_' not in self.juego.obtener_tablero():
            palabra = random.choice(self.palabras)
            self.palabras.remove(palabra)
            self.juego.palabra = palabra
            self.juego.tablero = ['_'] * len(palabra)

        # Si se agotan las palabras, termina el juego
        if self.juego.juego_perdido_estado == True:
            mostrar_mensaje("No hay más palabras disponibles.", BLACK)
            pygame.quit()
            sys.exit()


    def run_game(self):
        running = True
        mostrar_boton_reinicio = False
        mostrar_boton_continue = False
        global button_image, music_playing

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        if music_playing:
                            pygame.mixer.music.pause()
                            button_image = music_off_image
                        else:
                            pygame.mixer.music.unpause()
                            button_image = music_on_image
                        music_playing = not music_playing
                    elif mostrar_boton_reinicio and restart_button_rect.collidepoint(event.pos):
                       self.reiniciar_juego()  # Reinicia todo el juego
                       mostrar_boton_reinicio = False
                    elif mostrar_boton_continue and continue_button_rect.collidepoint(event.pos):
                        self.nueva_ronda()
                        mostrar_boton_continue = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Verificar si se presiona Enter
                        if mostrar_boton_reinicio:
                            self.juego.sumar_punto()
                            self.reiniciar_juego()
                            mostrar_boton_reinicio = False
                        elif mostrar_boton_continue:
                            self.nueva_ronda()
                            mostrar_boton_continue = False
                    elif not mostrar_boton_reinicio and not mostrar_boton_continue:
                        letra = event.unicode.lower()
                        if letra.isalpha() and letra not in self.juego.tablero and letra not in self.juego.letras_erroneas:
                            self.juego.adivinar(letra)
                            #if self.juego.juego_terminado():
                            #    if self.juego.juego_ganado():
                            #        mostrar_boton_continue = True
                            #    if self.juego.juego_perdido:
                            #        mostrar_boton_reinicio = True


            screen.fill(WHITE)
            screen.blit(button_image, button_rect.topleft)
            self.dibujar_juego()

            if self.juego.juego_terminado():
                font = pygame.font.Font(None, 42)
                if self.juego.juego_ganado():
                    texto = font.render('¡Ganaste!', True, BLACK)
                    screen.fill(VERDE)
                    mostrar_boton_continue = True
                if self.juego.juego_perdido():
                    texto = font.render('¡Perdiste!', True, BLACK)
                    screen.fill(ROJO)
                    texto2 = font.render('Palabra: ' + self.juego.obtener_palabra(), True, BLACK)
                    screen.blit(texto2, (40, 60))
                    mostrar_boton_reinicio = True
                screen.blit(texto, (100, 300))



            if mostrar_boton_reinicio:
                screen.blit(restart_button_image, restart_button_rect.topleft)
            if mostrar_boton_continue:
                screen.blit(continue_button_image, continue_button_rect.topleft)

            pygame.display.flip()

    def dibujar_juego(self):
        font = pygame.font.Font(None, 74)
        texto = font.render(self.juego.obtener_tablero(), True, BLACK)
        screen.blit(texto, (190, 140))

        font = pygame.font.Font(None, 24)
        texto = font.render('Partidas perdidas: ' + str(self.juego.partidasPerdidas), True, BLACK)
        screen.blit(texto, (screen.get_width() - 260, 25))

        font = pygame.font.Font(None, 36)
        texto = font.render('Letras erróneas: ' + self.juego.obtener_letras_erroneas(), True, BLACK)
        screen.blit(texto, (40, 230))

        print(f"Estado del ahorcado actual: {self.juego.ahorcado_estado}")
        if 0 <= self.juego.ahorcado_estado < len(self.ahorcado_images):
            screen.blit(self.ahorcado_images[self.juego.ahorcado_estado], (40, 50))
        else:
            print(f"Estado del ahorcado ({self.juego.ahorcado_estado}) fuera de rango.")

        font = pygame.font.Font(None, 25)
        texto = font.render('Puntos: ' + str(self.juego.puntos), True, BLACK)
        screen.blit(texto, (30, 30))

        for i in range(self.juego.vidas):
            screen.blit(vida_image, (30 + i * 30, 5))

if __name__ == '__main__':
    Juego('normal')  # Cambia 'normal' por 'dificil' según la selección
