import pygame


class AreaExplosion:

    def __init__(self, x, y, danio=15):
        self.x = x
        self.y = y
        self.radio = 20
        self.radio_max = 75
        self.danio = danio
        self.frame = 0
        self.max_frames = 30
        self.activa = True

    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio,
                           self.radio * 2, self.radio * 2)

    def update(self):
        self.frame += 1
        progreso = self.frame / self.max_frames
        if progreso < 0.4:
            self.radio = int(20 + (self.radio_max - 20) * (progreso / 0.4))
        else:
            self.radio = int(self.radio_max * (1 - (progreso - 0.4) / 0.6))
        if self.frame >= self.max_frames:
            self.activa = False

    def draw(self, pantalla):
        if not self.activa:
            return
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(pantalla, (255, 80, 0), (cx, cy), self.radio + 6, 2)
        pygame.draw.circle(pantalla, (255, 150, 0), (cx, cy), self.radio + 2, 2)
        pygame.draw.circle(pantalla, (255, 200, 50), (cx, cy), self.radio, 2)
        if self.radio > 10:
            pygame.draw.circle(pantalla, (255, 100, 20), (cx, cy), self.radio - 4)


class Explosion:

    def __init__(self, x, y):
        self.image_base = pygame.image.load(
            "assets/PNG/Sprites/Effects/spaceEffects_012.png"
        ).convert_alpha()
        self.frame = 0
        self.max_frames = 10
        self.activa = True
        self.x = x
        self.y = y

    def update(self):
        self.frame += 1
        if self.frame >= self.max_frames:
            self.activa = False

    def draw(self, pantalla):
        if not self.activa:
            return
        escala = 0.8 + self.frame * 0.5
        size = int(32 * escala)
        img = pygame.transform.scale(self.image_base, (size, size))
        rect = img.get_rect(center=(self.x, self.y))
        pantalla.blit(img, rect)
