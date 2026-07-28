import pygame
from src.config import ALTO


class Bullet:

    def __init__(self, x, y, velocidad=-8):
        self.velocidad = velocidad
        self.activa = True

        if velocidad < 0:
            img = pygame.image.load(
                "assets/PNG/Sprites/Missiles/spaceMissiles_001.png"
            ).convert_alpha()
        else:
            img = pygame.image.load(
                "assets/PNG/Sprites/Missiles/spaceMissiles_012.png"
            ).convert_alpha()
            img = pygame.transform.flip(img, False, True)

        self.image = pygame.transform.scale(img, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))

    def get_rect(self):
        return self.rect

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.activa = False

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
