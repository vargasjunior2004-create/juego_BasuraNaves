import pygame
from src.config import ANCHO, ALTO


class Boss:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tipo = 1

        img = pygame.image.load(
            "assets/PNG/Sprites/Ships/spaceShips_005.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -self.rect.height

        self.vida_maxima = 20 * nivel
        self.vida = self.vida_maxima
        self.velocidad_x = 2
        self.direccion = 1
        self.posicion_batalla_y = 80
        self.ultimo_disparo = 0
        self.cooldown_disparo = 600
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        # Ataque especial: rayo de plasma
        self.modo_especial = False
        self.ataques_normales = 0
        self.ataques_para_especial = 4
        self.fase_especial = ""
        self.timer_fase = 0
        self.ancho_rayo = 28

    def get_rect(self):
        return self.rect.inflate(-10, -10)

    def iniciar_especial(self):
        self.modo_especial = True
        self.fase_especial = "telegraph"
        self.timer_fase = 60

    def get_beam_rect(self):
        if not self.modo_especial or self.fase_especial != "beam":
            return None
        return pygame.Rect(
            self.rect.centerx - self.ancho_rayo // 2,
            self.rect.bottom,
            self.ancho_rayo,
            ALTO - self.rect.bottom
        )

    def update(self, jugador_x, ahora):
        if self.modo_especial:
            diff = jugador_x - self.rect.centerx
            if abs(diff) > 5:
                vel = self.velocidad_x * 1.5
                self.rect.x += vel if diff > 0 else -vel
            self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

            self.timer_fase -= 1
            if self.timer_fase <= 0:
                if self.fase_especial == "telegraph":
                    self.fase_especial = "beam"
                    self.timer_fase = 300
                elif self.fase_especial == "beam":
                    self.modo_especial = False
                    self.fase_especial = ""
                    self.ataques_normales = 0
            return

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
        if not self.activo or not self.en_posicion or self.modo_especial:
            return False
        if ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            self.ataques_normales += 1
            if self.ataques_normales >= self.ataques_para_especial:
                self.iniciar_especial()
            return True
        return False

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

        if self.inmune:
            t = pygame.time.get_ticks() // 80
            pulso = (t % 6) - 2
            radio = 48 + pulso
            pygame.draw.circle(pantalla, (100, 200, 255),
                               self.rect.center, radio + 6, 2)
            pygame.draw.circle(pantalla, (150, 230, 255),
                               self.rect.center, radio, 2)
            pygame.draw.circle(pantalla, (200, 240, 255),
                               self.rect.center, radio - 4, 1)

        if self.modo_especial:
            cx = self.rect.centerx
            by = self.rect.bottom
            bw = self.ancho_rayo
            bh = ALTO - by

            if self.fase_especial == "telegraph":
                t = pygame.time.get_ticks() // 100
                if t % 2 == 0:
                    pygame.draw.rect(pantalla, (255, 0, 0),
                                     (cx - bw // 2, by, bw, bh))

            elif self.fase_especial == "beam":
                pg = pygame.draw.rect
                pg(pantalla, (60, 20, 100), (cx - bw // 2 - 10, by, bw + 20, bh))
                pg(pantalla, (120, 40, 180), (cx - bw // 2 - 4, by, bw + 8, bh))
                pg(pantalla, (200, 100, 240), (cx - bw // 2 - 1, by, bw + 2, bh))
                pg(pantalla, (255, 230, 255), (cx - bw // 2, by, bw, bh))
