import pygame
import random
import math
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

        # Al pasar la zona de combate da la vuelta y regresa
        self.estado = "bajando"
        self.fase_regreso = 0
        self.vel_regreso = self.velocidad
        self.lado = 1
        self.vueltas = random.randint(1, 3)

    def get_rect(self):
        return self.rect.inflate(-6, -6)

    def update(self):
        if self.estado == "bajando":
            self.rect.y += self.velocidad
            if self.rect.top > ALTO - 120:
                self.estado = "regresando"
                self.fase_regreso = 0
                self.vel_regreso = self.velocidad
                self.lado = random.choice([-1, 1])
                self.velocidad = self.velocidad * 0.8
        else:  # regresando: gira, sube en curva y vuelve a entrar
            self.fase_regreso += 1
            self.rect.y -= self.velocidad
            self.rect.x += math.sin(self.fase_regreso * 0.06) * self.lado * 3
            self.rect.x += self.lado * 1.5
            self.rect.x = max(10, min(ANCHO - 10 - self.rect.width,
                                      self.rect.x))
            if self.rect.bottom < -20:
                self.vueltas -= 1
                if self.vueltas > 0:
                    self.estado = "bajando"
                    self.rect.y = -self.rect.height
                    self.velocidad = self.vel_regreso
                else:
                    self.activo = False

    def debe_disparar(self, ahora):
        if (self.activo and self.estado == "bajando"
                and ahora - self.ultimo_disparo >= self.cooldown_disparo):
            self.ultimo_disparo = ahora
            return True
        return False

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
