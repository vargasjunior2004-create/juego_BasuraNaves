import pygame
import math
from src.config import ANCHO, ALTO


class Boss:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tipo = 1
        self.habilidad_otorgada = 1

        base = "assets/asset_jefe 1"
        escala = 240 / 1096
        img_tent = pygame.image.load(
            f"{base}/ojo_01_tentaculos.png").convert_alpha()
        img_cuerpo = pygame.image.load(
            f"{base}/ojo_02_cuerpo.png").convert_alpha()
        img_boca = pygame.image.load(
            f"{base}/ojo_03_boca_dientes.png").convert_alpha()

        self.tentaculos_orig = pygame.transform.smoothscale(
            img_tent, (int(img_tent.get_width() * escala),
                       int(img_tent.get_height() * escala)))
        self.cuerpo = pygame.transform.smoothscale(
            img_cuerpo, (int(img_cuerpo.get_width() * escala),
                         int(img_cuerpo.get_height() * escala)))
        self.boca_base = pygame.transform.smoothscale(
            img_boca, (int(img_boca.get_width() * escala),
                       int(img_boca.get_height() * escala)))

        self.pos = pygame.Vector2(ANCHO // 2, -120)
        self.rect = pygame.Rect(0, 0, 130, 120)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.vida_maxima = 40 * nivel
        self.vida = self.vida_maxima
        self.velocidad_x = 2
        self.direccion = 1
        self.posicion_batalla_y = 110
        self.ultimo_disparo = 0
        self.cooldown_disparo = 800
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        # Animacion
        self.t = 0
        self.offset_y = 0

        # Ataque especial: rayo de plasma (se mantiene)
        self.modo_especial = False
        self.ataques_normales = 0
        self.ataques_para_especial = 4
        self.fase_especial = ""
        self.timer_fase = 0
        self.ancho_rayo = 28

        # Ataque basico: bola acido
        self.bolas_acido = []

    def get_rect(self):
        return self.rect.inflate(-20, -20)

    def iniciar_especial(self):
        self.modo_especial = True
        self.fase_especial = "telegraph"
        self.timer_fase = 60

    def get_beam_rect(self):
        if not self.modo_especial or self.fase_especial != "beam":
            return None
        y0 = int(self.pos.y) + 30
        return pygame.Rect(
            int(self.pos.x) - self.ancho_rayo // 2,
            y0,
            self.ancho_rayo,
            ALTO - y0
        )

    def update(self, jugador_x, ahora):
        self.t += 1

        if self.modo_especial:
            diff = jugador_x - self.pos.x
            if abs(diff) > 5:
                vel = self.velocidad_x * 1.6
                self.pos.x += vel if diff > 0 else -vel
            self.pos.x = max(60, min(ANCHO - 60, self.pos.x))

            self.timer_fase -= 1
            if self.timer_fase <= 0:
                if self.fase_especial == "telegraph":
                    self.fase_especial = "beam"
                    self.timer_fase = 300
                elif self.fase_especial == "beam":
                    self.modo_especial = False
                    self.fase_especial = ""
                    self.ataques_normales = 0
        else:
            if not self.en_posicion:
                self.pos.y += 2
                if self.pos.y >= self.posicion_batalla_y:
                    self.pos.y = self.posicion_batalla_y
                    self.en_posicion = True
            else:
                self.pos.x += self.velocidad_x * self.direccion
                if self.pos.x >= ANCHO - 100:
                    self.direccion = -1
                elif self.pos.x <= 100:
                    self.direccion = 1
                self.offset_y = math.sin(self.t * 0.03) * 10
                self.pos.y = self.posicion_batalla_y + self.offset_y

        self.rect.center = (int(self.pos.x), int(self.pos.y))

        for b in self.bolas_acido[:]:
            b.update()
            if not b.activa:
                self.bolas_acido.remove(b)

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
        cx = int(self.pos.x)
        cy = int(self.pos.y)

        # Tentaculos con balanceo (mas amplio durante el especial)
        if self.modo_especial:
            swing = math.sin(self.t * 0.1) * 14
        else:
            swing = math.sin(self.t * 0.04) * 8
        tent_img = pygame.transform.rotate(self.tentaculos_orig, swing)
        pantalla.blit(tent_img, tent_img.get_rect(center=(cx, cy)))

        # Cuerpo
        pantalla.blit(self.cuerpo, self.cuerpo.get_rect(center=(cx, cy)))

        # Boca/dientes, que se abre durante el especial
        boca_img = self.boca_base
        if self.modo_especial:
            pulso = 1.0 + math.sin(self.t * 0.2) * 0.15
            w = int(self.boca_base.get_width() * pulso)
            h = int(self.boca_base.get_height() * pulso)
            if w > 0 and h > 0:
                boca_img = pygame.transform.smoothscale(self.boca_base, (w, h))
        pantalla.blit(boca_img, boca_img.get_rect(center=(cx, cy)))

        for b in self.bolas_acido:
            b.draw(pantalla)

        if self.inmune:
            t = pygame.time.get_ticks() // 80
            pulso = (t % 6) - 2
            radio = 48 + pulso
            pygame.draw.circle(pantalla, (100, 200, 255),
                               (cx, cy), radio + 6, 2)
            pygame.draw.circle(pantalla, (150, 230, 255),
                               (cx, cy), radio, 2)
            pygame.draw.circle(pantalla, (200, 240, 255),
                               (cx, cy), radio - 4, 1)

        if self.modo_especial:
            by = cy + 30
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
