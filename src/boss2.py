import pygame
from src.config import ANCHO, ALTO


class Boss2:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tipo = 2
        self.habilidad_otorgada = 2

        img = pygame.image.load(
            "assets/PNG/Sprites/Ships/spaceShips_003.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -self.rect.height

        self.vida_maxima = 40 * nivel
        self.vida = self.vida_maxima
        self.velocidad_x = 2
        self.direccion = 1
        self.posicion_batalla_y = 80
        self.ultimo_disparo = 0
        self.cooldown_disparo = 150
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        self.ataques_normales = 0
        self.ataques_para_especial = 10
        self.es_disparo_especial = False
        self.energy_balls = []

    def get_rect(self):
        return self.rect.inflate(-10, -10)

    def get_beam_rect(self):
        return None

    def update(self, jugador_x, ahora):
        if not self.en_posicion:
            self.rect.y += 2
            if self.rect.y >= self.posicion_batalla_y:
                self.rect.y = self.posicion_batalla_y
                self.en_posicion = True
        else:
            self.rect.x += self.velocidad_x * self.direccion
            if self.rect.right >= ANCHO - 20:
                self.direccion = -1
            elif self.rect.left <= 20:
                self.direccion = 1

    def debe_disparar(self, ahora):
        if not self.activo or not self.en_posicion:
            return False
        if ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            self.ataques_normales += 1
            if self.ataques_normales >= self.ataques_para_especial:
                self.ataques_normales = 0
                self.es_disparo_especial = True
            return True
        return False

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

        if self.inmune:
            t = pygame.time.get_ticks() // 80
            pulso = (t % 6) - 2
            radio = 48 + pulso
            pygame.draw.circle(pantalla, (255, 100, 100),
                               self.rect.center, radio + 6, 2)
            pygame.draw.circle(pantalla, (255, 150, 150),
                               self.rect.center, radio, 2)
            pygame.draw.circle(pantalla, (255, 200, 200),
                               self.rect.center, radio - 4, 1)

        for ball in self.energy_balls:
            ball.draw(pantalla)
