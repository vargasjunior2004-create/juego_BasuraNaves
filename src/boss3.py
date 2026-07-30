import pygame
from src.config import ANCHO


class Boss3:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tipo = 3

        img = pygame.image.load(
            "assets/alien-ufo-pack/PNG/shipBlue_manned.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (90, 65))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -self.rect.height

        self.vida_maxima = 20 * nivel
        self.vida = self.vida_maxima
        self.velocidad_x = 2
        self.direccion = 1
        self.posicion_batalla_y = 80
        self.ultimo_disparo = 0
        self.cooldown_entre_rafagas = 1800
        self.cooldown_entre_disparos = 120
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        self.rafaga_activa = False
        self.disparos_restantes_rafaga = 0
        self.rafagas_completadas = 0
        self.refuerzos_pendientes = False

    def get_rect(self):
        return self.rect.inflate(-10, -10)

    def get_beam_rect(self):
        return None

    def update(self, jugador_x, ahora):
        if not self.en_posicion:
            self.rect.y += 2
            if self.rect.y >= self.posicion_batalla_y:
                self.rect.y = self.posicion_batalla_y
                self.en_posicion = True
        else:
            self.rect.x += self.velocidad_x * self.direccion
            if self.rect.right >= ANCHO - 20:
                self.direccion = -1
            elif self.rect.left <= 20:
                self.direccion = 1

    def debe_disparar(self, ahora):
        if not self.activo or not self.en_posicion:
            return False

        if self.rafaga_activa:
            if ahora - self.ultimo_disparo >= self.cooldown_entre_disparos:
                self.ultimo_disparo = ahora
                self.disparos_restantes_rafaga -= 1
                if self.disparos_restantes_rafaga <= 0:
                    self.rafaga_activa = False
                    self.rafagas_completadas += 1
                    if self.rafagas_completadas % 3 == 0:
                        self.refuerzos_pendientes = True
                return True
            return False
        else:
            if ahora - self.ultimo_disparo < self.cooldown_entre_rafagas:
                return False
            self.rafaga_activa = True
            self.disparos_restantes_rafaga = 3
            self.ultimo_disparo = ahora
            self.disparos_restantes_rafaga -= 1
            return True

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

        if self.inmune:
            t = pygame.time.get_ticks() // 80
            pulso = (t % 6) - 2
            radio = 52 + pulso
            pygame.draw.circle(pantalla, (100, 100, 255),
                               self.rect.center, radio + 6, 2)
            pygame.draw.circle(pantalla, (150, 150, 255),
                               self.rect.center, radio, 2)
            pygame.draw.circle(pantalla, (200, 200, 255),
                               self.rect.center, radio - 4, 1)
