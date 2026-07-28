import pygame
from src.config import ANCHO, ALTO


class Player:

    def __init__(self):
        img = pygame.image.load(
            "assets/PNG/Sprites/Ships/spaceShips_001.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 80

        self.velocidad = 5
        self.vida_maxima = 100
        self.vida = 100
        self.ultimo_disparo = 0
        self.cooldown_disparo = 250
        self.poder_activo = False
        self.tiempo_inicio_poder = 0
        self.duracion_poder = 8000

    def get_rect(self):
        return self.rect.inflate(-10, -10)

    def update(self, teclas, ahora):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidad

        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

        if self.poder_activo and ahora - self.tiempo_inicio_poder >= self.duracion_poder:
            self.poder_activo = False

    def disparar(self, ahora):
        if ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            return True
        return False

    def activar_poder(self):
        self.poder_activo = True
        self.tiempo_inicio_poder = pygame.time.get_ticks()

    def draw(self, pantalla):
        if self.poder_activo:
            pygame.draw.circle(pantalla, (255, 255, 0),
                               self.rect.center, 30, 3)
        pantalla.blit(self.image, self.rect)
