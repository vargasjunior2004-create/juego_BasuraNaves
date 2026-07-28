import pygame


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
