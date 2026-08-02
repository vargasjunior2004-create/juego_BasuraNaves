import pygame
import math
from src.config import ANCHO, ALTO


class BolaAcido:
    """Bola de acido del jefe 1: se lanza hacia el jugador y pulsa mientras cae."""

    def __init__(self, x, y, destino, nivel):
        self.x = x
        self.y = y
        self.nivel = nivel
        self.danio = 12
        self.activa = True
        self.t = 0

        img = pygame.image.load(
            "assets/asset_jefe 1/ojo_05_bola_acido.png"
        ).convert_alpha()
        self.img_orig = pygame.transform.smoothscale(img, (46, 46))
        self.img = self.img_orig

        dx = destino[0] - x
        dy = destino[1] - y
        d = math.hypot(dx, dy)
        vel = 4 + nivel * 0.2
        if d > 0:
            self.vx = dx / d * vel
            self.vy = dy / d * vel
        else:
            self.vx, self.vy = 0, vel

    def get_rect(self):
        return pygame.Rect(self.x - 18, self.y - 18, 36, 36)

    def update(self):
        self.t += 1
        self.x += self.vx
        self.y += self.vy

        pulso = 1.0 + math.sin(self.t * 0.3) * 0.15
        w = int(self.img_orig.get_width() * pulso)
        h = int(self.img_orig.get_height() * pulso)
        if w > 0 and h > 0:
            self.img = pygame.transform.smoothscale(self.img_orig, (w, h))

        if (self.y > ALTO + 40 or self.y < -40
                or self.x < -40 or self.x > ANCHO + 40):
            self.activa = False

    def draw(self, pantalla):
        r = self.img.get_rect(center=(int(self.x), int(self.y)))
        pantalla.blit(self.img, r)
