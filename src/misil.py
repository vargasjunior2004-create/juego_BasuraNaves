import pygame
import math


class MisilInteligente:

    def __init__(self, x, y, px, py, velocidad=4.0, turno=0.06,
                 vida_max=180, danio=15, color=(255, 90, 120)):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.turno = turno
        self.vida = vida_max
        self.vida_max = vida_max
        self.danio = danio
        self.color = color
        self.activo = True
        self.rastro = []

        dx = px - x
        dy = py - y
        d = math.hypot(dx, dy)
        if d > 0:
            self.vx = dx / d * self.velocidad
            self.vy = dy / d * self.velocidad
        else:
            self.vx, self.vy = 0, -self.velocidad

    def update(self, px, py):
        if not self.activo:
            return
        dx = px - self.x
        dy = py - self.y
        d = math.hypot(dx, dy)
        if d > 0:
            obj_vx = dx / d * self.velocidad
            obj_vy = dy / d * self.velocidad
        else:
            obj_vx, obj_vy = self.vx, self.vy
        self.vx += (obj_vx - self.vx) * self.turno
        self.vy += (obj_vy - self.vy) * self.turno
        norm = math.hypot(self.vx, self.vy)
        if norm > 0:
            self.vx = self.vx / norm * self.velocidad
            self.vy = self.vy / norm * self.velocidad
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1

        self.rastro.append((int(self.x), int(self.y)))
        if len(self.rastro) > 12:
            self.rastro.pop(0)

        if self.vida <= 0:
            self.activo = False

    def get_rect(self):
        return pygame.Rect(int(self.x - 8), int(self.y - 8), 16, 16)

    def draw(self, pantalla):
        if not self.activo:
            return
        largo = len(self.rastro)
        for i, (rx, ry) in enumerate(self.rastro):
            radio = max(1, int(5 * (i + 1) / largo))
            pygame.draw.circle(pantalla, self.color, (rx, ry), radio)
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), 7)
        pygame.draw.circle(pantalla, (255, 255, 255),
                           (int(self.x), int(self.y)), 4)
