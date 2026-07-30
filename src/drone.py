import pygame
import math


class AlienDrone:

    def __init__(self, x, y, jugador_x, jugador_y):
        img = pygame.image.load(
            "assets/alien-ufo-pack/PNG/shipGreen.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (32, 18))
        self.x = x
        self.y = y
        self.ancho = 32
        self.alto = 18
        self.vel = 2.5
        self.vida = 1
        self.activo = True

        dx = jugador_x - x
        dy = jugador_y - y
        d = math.hypot(dx, dy)
        if d > 0:
            self.vx = dx / d * self.vel
            self.vy = dy / d * self.vel
        else:
            self.vx, self.vy = 0, self.vel

    def update(self, jugador_x, jugador_y):
        dx = jugador_x - self.x
        dy = jugador_y - self.y
        d = math.hypot(dx, dy)
        if d > 0:
            self.vx += (dx / d * self.vel - self.vx) * 0.05
            self.vy += (dy / d * self.vel - self.vy) * 0.05
        self.x += self.vx
        self.y += self.vy

        if self.y > 700 or self.x < -50 or self.x > 530:
            self.activo = False

    def draw(self, pantalla):
        if self.activo:
            pantalla.blit(self.image, (int(self.x - self.ancho // 2),
                                       int(self.y - self.alto // 2)))

    def get_rect(self):
        return pygame.Rect(int(self.x - self.ancho // 2),
                           int(self.y - self.alto // 2),
                           self.ancho, self.alto)
