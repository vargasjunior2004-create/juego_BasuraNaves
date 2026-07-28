import pygame
import random
from src.config import ANCHO, ALTO


class Enemy:

    def __init__(self):
        num = random.choice(["004", "009"])
        img = pygame.image.load(
            f"assets/PNG/Sprites/Ships/spaceShips_{num}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, ANCHO - 30 - self.rect.width)
        self.rect.y = -self.rect.height

        self.velocidad = random.uniform(1.5, 3.5)
        self.ultimo_disparo = 0
        self.cooldown_disparo = random.randint(1500, 3000)
        self.activo = True

    def get_rect(self):
        return self.rect.inflate(-6, -6)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO + 50:
            self.activo = False

    def debe_disparar(self, ahora):
        if self.activo and ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            return True
        return False

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
