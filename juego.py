import random

class Ahorcado:
    def __init__(self, palabras, ahorcado_images):
        self.palabras = palabras
        self.ahorcado_images = ahorcado_images
        self.partidasPerdidas=0
        self.palabras_jugadas = []  # Reiniciar las palabras jugadas
        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.vidas = 3  # Reiniciar las vidas
        self.puntos = 0  # Reiniciar los puntos
        self.intentos = 7
        self.ahorcado_estado = 0
        self.juego_perdido_estado = False  # Reiniciar el estado de juego perdido
        self.nueva_ronda()

    def nueva_ronda(self):
        palabras_disponibles = [palabra for palabra in self.palabras if palabra not in self.palabras_jugadas]
        if not palabras_disponibles:
            print("No hay más palabras disponibles.")
            self.juego_perdido_estado = True  # Establece el estado del juego como perdido
            return
        self.palabra = random.choice(palabras_disponibles)
        self.palabras_jugadas.append(self.palabra)
        self.tablero = ['_'] * len(self.palabra)
        self.letras_erroneas = []

    def obtener_tablero(self):
        return ' '.join(self.tablero)

    def obtener_letras_erroneas(self):
        return ', '.join(self.letras_erroneas)

    def adivinar(self, letra):
        if letra in self.palabra:
            for idx, char in enumerate(self.palabra):
                if char == letra:
                    self.tablero[idx] = letra
        else:
            self.letras_erroneas.append(letra)
            self.ahorcado_estado = min(self.ahorcado_estado + 1, len(self.ahorcado_images) - 1)
            self.intentos -= 1
            if self.intentos <= 0:
                self.perder_vidas()


    def perder_vidas(self):
        if self.vidas > 0:
            self.vidas -= 1
        if self.vidas <= 0:
            self.juego_perdido_estado = True

    def juego_terminado(self):
        return self.juego_ganado() or self.juego_perdido()

    def juego_ganado(self):
        return '_' not in self.tablero

    def juego_perdido(self):
        return self.ahorcado_estado >= len(self.ahorcado_images) or self.juego_perdido_estado

    def sumar_perdidas(self):
        self.partidasPerdidas += 1

    def sumar_punto(self):
        self.puntos += 1

    def obtener_puntos(self):
        return self.puntos

    def obtener_palabra(self):
        return self.palabra

    def obtener_vidas(self):
        return self.vidas
