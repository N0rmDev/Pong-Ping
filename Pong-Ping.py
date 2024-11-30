import pygame
import random

# Inicializa Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong")

# Colores
BLANCO_MAS_CLARO = (255, 255, 240)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)

# Configuraciones del juego
FPS = 60
VELOCIDAD_PELOTA = 5
ANCHO_RAQUETA, ALTO_RAQUETA = 20, 100
VELOCIDAD_RAQUETA = 7
PROB_ERROR = 0.5

# Fuente
FUENTE = pygame.font.SysFont("Arial", 36, bold=True)
FUENTE_BOTON = pygame.font.SysFont("Arial", 28, bold=True)

# Clases
class Raqueta:
    def __init__(self, x, y, color):
        self.inicio_x = x
        self.inicio_y = y
        self.rect = pygame.Rect(x, y, ANCHO_RAQUETA, ALTO_RAQUETA)
        self.color = color
        self.velocidad = VELOCIDAD_RAQUETA

    def mover(self, arriba=True):
        if arriba:
            self.rect.y -= self.velocidad
        else:
            self.rect.y += self.velocidad

    def dibujar(self):
        pygame.draw.rect(VENTANA, self.color, self.rect)

    def reset(self):
        self.rect.topleft = (self.inicio_x, self.inicio_y)


class Pelota:
    def __init__(self):
        self.rect = pygame.Rect(ANCHO // 2 - 15, ALTO // 2 - 15, 30, 30)
        self.vel_x = VELOCIDAD_PELOTA * random.choice((1, -1))
        self.vel_y = VELOCIDAD_PELOTA * random.choice((1, -1))

    def mover(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.y <= 100 or self.rect.y >= ALTO - 30:
            self.vel_y *= -1

    def dibujar(self):
        pygame.draw.ellipse(VENTANA, NEGRO, self.rect)

    def reset(self):
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.vel_x = VELOCIDAD_PELOTA * random.choice((1, -1))
        self.vel_y = VELOCIDAD_PELOTA * random.choice((1, -1))


def pantalla_final(ganador):
    """Pantalla de ganar o perder con botones para reiniciar o salir"""
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        VENTANA.fill(BLANCO_MAS_CLARO)

        # Mensaje de victoria o derrota
        if ganador == "Jugador":
            mensaje = "¡Felicidades! ¡Has ganado!"
        else:
            mensaje = "Jaja, perdiste contra un botsito."

        texto_mensaje = FUENTE.render(mensaje, True, NEGRO)
        VENTANA.blit(texto_mensaje, (ANCHO // 2 - texto_mensaje.get_width() // 2, ALTO // 4))

        # Botones de "Reiniciar" y "Salir"
        boton_reiniciar = pygame.Rect(ANCHO // 3 - 60, ALTO // 2, 120, 50)
        boton_salir = pygame.Rect(2 * ANCHO // 3 - 60, ALTO // 2, 120, 50)

        pygame.draw.rect(VENTANA, AZUL, boton_reiniciar)
        pygame.draw.rect(VENTANA, ROJO, boton_salir)

        texto_reiniciar = FUENTE_BOTON.render("Reiniciar", True, BLANCO_MAS_CLARO)
        texto_salir = FUENTE_BOTON.render("Salir", True, BLANCO_MAS_CLARO)

        VENTANA.blit(
            texto_reiniciar,
            (boton_reiniciar.centerx - texto_reiniciar.get_width() // 2,
             boton_reiniciar.centery - texto_reiniciar.get_height() // 2),
        )
        VENTANA.blit(
            texto_salir,
            (boton_salir.centerx - texto_salir.get_width() // 2,
             boton_salir.centery - texto_salir.get_height() // 2),
        )

        # Detectar clics
        pos_mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if boton_reiniciar.collidepoint(pos_mouse):
                return True  # Reiniciar el juego
            if boton_salir.collidepoint(pos_mouse):
                return False  # Salir del juego

        pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    pelota = Pelota()
    raqueta1 = Raqueta(30, ALTO // 2 - ALTO_RAQUETA // 2, AZUL)
    raqueta2 = Raqueta(ANCHO - 30 - ANCHO_RAQUETA, ALTO // 2 - ALTO_RAQUETA // 2, ROJO)

    puntaje_jugador = 0
    puntaje_bot = 0

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and raqueta1.rect.top > 100:
            raqueta1.mover(arriba=True)
        if teclas[pygame.K_s] and raqueta1.rect.bottom < ALTO:
            raqueta1.mover(arriba=False)

        if pelota.vel_x > 0:
            if random.random() > PROB_ERROR:
                if raqueta2.rect.centery < pelota.rect.centery and raqueta2.rect.bottom < ALTO:
                    raqueta2.mover(arriba=False)
                if raqueta2.rect.centery > pelota.rect.centery and raqueta2.rect.top > 100:
                    raqueta2.mover(arriba=True)

        pelota.mover()

        if pelota.rect.colliderect(raqueta1.rect) or pelota.rect.colliderect(raqueta2.rect):
            pelota.vel_x *= -1

        if pelota.rect.left <= 0 or pelota.rect.right >= ANCHO:
            if pelota.rect.left <= 0:
                puntaje_bot += 1
            else:
                puntaje_jugador += 1

            pelota.reset()
            raqueta1.reset()
            raqueta2.reset()

            if puntaje_jugador >= 5:
                if not pantalla_final("Jugador"):
                    ejecutando = False
                puntaje_jugador, puntaje_bot = 0, 0

            elif puntaje_bot >= 5:
                if not pantalla_final("Bot"):
                    ejecutando = False
                puntaje_jugador, puntaje_bot = 0, 0

        # Dibujar
        VENTANA.fill(BLANCO_MAS_CLARO)
        pygame.draw.rect(VENTANA, GRIS, pygame.Rect(0, 0, ANCHO, 100))
        pygame.draw.line(VENTANA, NEGRO, (0, 100), (ANCHO, 100), 3)

        texto_puntaje_jugador = FUENTE.render(str(puntaje_jugador), True, AZUL)
        texto_puntaje_bot = FUENTE.render(str(puntaje_bot), True, ROJO)
        texto_score = FUENTE.render("SCORE", True, NEGRO)

        VENTANA.blit(texto_puntaje_jugador, (ANCHO // 4, 30))
        VENTANA.blit(texto_puntaje_bot, (3 * ANCHO // 4, 30))
        VENTANA.blit(texto_score, (ANCHO // 2 - texto_score.get_width() // 2, 30))

        raqueta1.dibujar()
        raqueta2.dibujar()
        pelota.dibujar()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
