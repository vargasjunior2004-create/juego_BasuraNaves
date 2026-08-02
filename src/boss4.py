import pygame
import random
from src.config import ANCHO
from src.misil import MisilInteligente


class Boss4:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tipo = 4
        self.habilidad_otorgada = 5

        img = pygame.image.load(
            "assets/alien-ufo-pack/PNG/shipPink_manned.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (90, 65))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -self.rect.height

        self.vida_maxima = 60 * nivel
        self.vida = self.vida_maxima
        self.velocidad_x = 2
        self.direccion = 1
        self.posicion_batalla_y = 80
        self.ultimo_disparo = 0
        self.cooldown_disparo = 2000
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        self.misiles = []

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
            return True
        return False

    def lanzar_misiles(self, player_pos):
        px, py = player_pos
        for dx in (-16, 0, 16):
            self.misiles.append(
                MisilInteligente(
                    self.rect.centerx + dx, self.rect.bottom + 5,
                    px, py,
                    velocidad=random.uniform(3.6, 4.2),
                    turno=0.06,
                    vida_max=random.randint(150, 210),
                    danio=15,
                    color=(255, 90, 120)))

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

        for m in self.misiles:
            m.draw(pantalla)

        if self.inmune:
            t = pygame.time.get_ticks() // 80
            pulso = (t % 6) - 2
            radio = 52 + pulso
            pygame.draw.circle(pantalla, (255, 120, 180),
                               self.rect.center, radio + 6, 2)
            pygame.draw.circle(pantalla, (255, 170, 200),
                               self.rect.center, radio, 2)
            pygame.draw.circle(pantalla, (255, 220, 235),
                               self.rect.center, radio - 4, 1)
