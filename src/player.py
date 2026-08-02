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

        self.escudo_activo = False
        self.tiempo_escudo = 0

        self.habilidad_tipo = 0
        self.habilidad_activa = False
        self.tiempo_habilidad = 0
        self.duracion_habilidad = 300

    def get_rect(self):
        return self.rect.inflate(-10, -10)

    def get_beam_rect(self):
        if not self.habilidad_activa or self.habilidad_tipo != 1:
            return None
        return pygame.Rect(
            self.rect.centerx - 14, 0, 28, self.rect.top
        )

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

        if self.escudo_activo:
            self.tiempo_escudo -= 1
            if self.tiempo_escudo <= 0:
                self.escudo_activo = False

    def disparar(self, ahora):
        if ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            return True
        return False

    def activar_poder(self):
        self.poder_activo = True

    def activar_escudo(self):
        self.escudo_activo = True
        self.tiempo_escudo = 600

    def draw(self, pantalla):
        if self.poder_activo:
            pygame.draw.circle(pantalla, (255, 255, 0),
                               self.rect.center, 30, 3)
        if self.escudo_activo:
            pygame.draw.circle(pantalla, (0, 180, 255),
                               self.rect.center, 36, 3)
            pygame.draw.circle(pantalla, (120, 220, 255),
                               self.rect.center, 40, 1)
        pantalla.blit(self.image, self.rect)
