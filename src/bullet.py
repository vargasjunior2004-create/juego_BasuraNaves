import pygame
import math
from src.config import ANCHO, ALTO


class Bullet:

    def __init__(self, x, y, velocidad=-8, vx=0, vy=None):
        self.velocidad = velocidad
        self.vx = vx
        self.vy = velocidad if vy is None else vy
        self.activa = True

        if self.vy < 0:
            img = pygame.image.load(
                "assets/PNG/Sprites/Missiles/spaceMissiles_001.png"
            ).convert_alpha()
        else:
            img = pygame.image.load(
                "assets/PNG/Sprites/Missiles/spaceMissiles_012.png"
            ).convert_alpha()
            img = pygame.transform.flip(img, False, True)

        self.image = pygame.transform.scale(img, (16, 16))
        if vx != 0:
            angulo = -math.degrees(math.atan2(vx, self.vy))
            self.image = pygame.transform.rotate(self.image, angulo)
        self.rect = self.image.get_rect(center=(x, y))

    def get_rect(self):
        return self.rect

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.bottom < 0 or self.rect.top > ALTO
                or self.rect.right < 0 or self.rect.left > ANCHO):
            self.activa = False

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
