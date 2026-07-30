import pygame
import math
from src.config import ALTO


class EnergyBall:

    def __init__(self, x, y, target_x, nivel):
        self.x = x
        self.y = y
        self.radio = 14
        self.activa = True
        self.explotada = False
        self._debe_explotar = False

        dx = target_x - x
        dy = ALTO + 50 - y
        dist = math.hypot(dx, dy)
        vel = 3.5
        self.vel_x = dx / dist * vel if dist > 0 else 0
        self.vel_y = dy / dist * vel if dist > 0 else vel

        self.tiempo_vida = 0
        self.vida_max = 150

    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio,
                           self.radio * 2, self.radio * 2)

    def update(self, jugador_y):
        if not self.activa:
            return

        self.x += self.vel_x
        self.y += self.vel_y
        self.tiempo_vida += 1

        self.radio = 14 + int(math.sin(self.tiempo_vida * 0.3) * 3)

        if not self.explotada:
            if self.y >= jugador_y - 40 or self.tiempo_vida >= self.vida_max:
                self.explotada = True
                self._debe_explotar = True

        if self.y > ALTO + 60 or self.tiempo_vida > self.vida_max + 20:
            self.activa = False

    def debe_explotar(self):
        if self._debe_explotar:
            self._debe_explotar = False
            return True
        return False

    def draw(self, pantalla):
        if not self.activa:
            return
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(pantalla, (255, 150, 0), (cx, cy), self.radio + 6, 2)
        pygame.draw.circle(pantalla, (255, 200, 0), (cx, cy), self.radio + 2, 2)
        pygame.draw.circle(pantalla, (255, 255, 200), (cx, cy), self.radio)
        pygame.draw.circle(pantalla, (255, 200, 50), (cx, cy), self.radio - 4)
