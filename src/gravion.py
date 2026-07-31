import pygame
import math
import random
from src.config import ANCHO, ALTO


class Gravion(pygame.sprite.Sprite):

    def __init__(self, nivel):
        super().__init__()
        self.nivel = nivel
        self.tipo = 5
        self.habilidad_otorgada = 4

        base = "assets/Gravion"
        img_cuerpo = pygame.image.load(f"{base}/gravion_01_cuerpo.png").convert_alpha()
        img_domo = pygame.image.load(f"{base}/gravion_02_domo_gravion.png").convert_alpha()
        img_nucleo = pygame.image.load(f"{base}/gravion_03_nucleo.png").convert_alpha()
        img_ast = pygame.image.load(f"{base}/gravion_04_asteroide.png").convert_alpha()

        self.body = pygame.transform.smoothscale(img_cuerpo, (140, 140))
        self.dome = pygame.transform.smoothscale(img_domo, (80, 80))
        self.nucleus_orig = pygame.transform.smoothscale(img_nucleo, (56, 56))
        self.nucleus_img = self.nucleus_orig
        self.ast_orig = pygame.transform.smoothscale(img_ast, (28, 28))

        self.pos = pygame.Vector2(ANCHO // 2, -100)
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.rect.center = (self.pos.x, self.pos.y)

        self.vida_maxima = 25 * nivel
        self.vida = self.vida_maxima
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        self.vel_x = 0
        self.dir = 1
        self.t = 0
        self.offset_y = 0

        self.asteroides = []
        for i in range(5):
            a = {
                "idx": i,
                "angle_deg": i * 72,
                "vel_ang": random.choice([-1, 1]) * random.uniform(0.4, 1.0),
                "rot": random.uniform(0, 360),
                "radius": 105,
                "attached": True,
                "x": 0, "y": 0,
                "vx": 0, "vy": 0,
                "regen": 0,
                "img": self.ast_orig,
            }
            self.asteroides.append(a)

        self.ultimo_disparo = 0
        self.cooldown_disparo = 2500

        self.ataques_normales = 0
        self.ataques_para_especial = 3
        self.estado = "idle"
        self.timer_estado = 0
        self.atraccion_activa = False
        self.fuerza_atraccion = 0
        self.onda_activa = False
        self.radio_onda = 0
        self.onda_centro = pygame.Vector2(0, 0)
        self.danio_onda = 8 * nivel
        self.vulnerable = False

    def get_rect(self):
        return self.rect

    def get_beam_rect(self):
        return None

    def iniciar_especial(self):
        self.estado = "charging"
        self.timer_estado = 120
        self.ataques_normales = 0

    def debe_disparar(self, ahora):
        if not self.activo or not self.en_posicion or self.estado != "idle":
            return False
        if ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            return True
        return False

    def update(self, dt, player_pos):
        self.t += 1
        player_vec = pygame.Vector2(player_pos) if isinstance(player_pos, (tuple, list)) else player_pos

        if not self.en_posicion:
            self.pos.y += 1.5
            if self.pos.y >= 90:
                self.pos.y = 90
                self.en_posicion = True
                self.vel_x = 1.5
        else:
            self.pos.x += self.vel_x * self.dir
            if self.pos.x >= ANCHO - 100:
                self.dir = -1
            elif self.pos.x <= 100:
                self.dir = 1
            self.offset_y = math.sin(self.t * 0.025) * 8
            self.pos.y = 90 + self.offset_y

        self.rect.center = (self.pos.x, self.pos.y)

        for a in self.asteroides:
            if a["attached"]:
                a["angle_deg"] = (a["angle_deg"] + a["vel_ang"]) % 360
                rad = math.radians(a["angle_deg"])
                a["x"] = self.pos.x + math.cos(rad) * a["radius"]
                a["y"] = self.pos.y + math.sin(rad) * a["radius"]
                a["rot"] += 2
            else:
                a["x"] += a["vx"]
                a["y"] += a["vy"]
                a["rot"] += 6

                if (a["y"] > ALTO + 60 or a["x"] < -60 or a["x"] > ANCHO + 60):
                    a["regen"] = 180

            if not a["attached"] and a["regen"] > 0:
                a["regen"] -= 1
                if a["regen"] == 0:
                    a["attached"] = True
                    a["angle_deg"] = self._calcular_angulo_libre()
                    a["radius"] = 105

        if self.estado != "idle":
            self.timer_estado -= 1
            if self.timer_estado <= 0:
                if self.estado == "charging":
                    self.estado = "pulling"
                    self.timer_estado = 180
                    self.atraccion_activa = True
                    self.fuerza_atraccion = 0
                elif self.estado == "pulling":
                    self.estado = "releasing"
                    self.timer_estado = 60
                    self.atraccion_activa = False
                    self.onda_activa = True
                    self.radio_onda = 10
                    self.onda_centro = pygame.Vector2(self.pos.x, self.pos.y + 20)
                elif self.estado == "releasing":
                    self.estado = "vulnerable"
                    self.timer_estado = 180
                    self.onda_activa = False
                    self.vulnerable = True
                elif self.estado == "vulnerable":
                    self.estado = "idle"
                    self.vulnerable = False
                    self.especial_cooldown = 300

        if self.estado == "pulling":
            self.fuerza_atraccion = min(8, self.fuerza_atraccion + 0.05)

        if self.estado == "releasing" and self.onda_activa:
            self.radio_onda += 12

        pulso = 1.0 + math.sin(self.t * 0.1) * 0.04
        if self.estado == "charging":
            pulso = 1.0 + math.sin(self.t * 0.25) * 0.08
        elif self.estado == "pulling":
            pulso = 1.0 + math.sin(self.t * 0.3) * 0.06
        elif self.estado == "vulnerable":
            pulso = 1.0 + math.sin(self.t * 0.15) * 0.03

        w = int(self.nucleus_orig.get_width() * pulso)
        h = int(self.nucleus_orig.get_height() * pulso)
        if w > 0 and h > 0:
            self.nucleus_img = pygame.transform.smoothscale(self.nucleus_orig, (w, h))

    def _calcular_angulo_libre(self):
        usados = [a["angle_deg"] for a in self.asteroides if a["attached"]]
        if not usados:
            return random.uniform(0, 360)
        usados.sort()
        huecos = []
        for i in range(len(usados)):
            sig = usados[(i + 1) % len(usados)]
            if i == len(usados) - 1:
                gap = (360 - usados[i] + sig)
            else:
                gap = sig - usados[i]
            huecos.append((gap, usados[i]))
        huecos.sort(reverse=True)
        mejor = huecos[0][1]
        return (mejor + huecos[0][0] / 2) % 360

    def lanzar_asteroide(self, player_pos):
        for a in self.asteroides:
            if a["attached"]:
                a["attached"] = False
                pv = pygame.Vector2(player_pos) if isinstance(player_pos, (tuple, list)) else player_pos
                dx = pv.x - a["x"]
                dy = pv.y - a["y"]
                d = math.hypot(dx, dy)
                vel = 5 + self.nivel * 0.3
                if d > 0:
                    a["vx"] = dx / d * vel
                    a["vy"] = dy / d * vel
                else:
                    a["vx"] = 0
                    a["vy"] = vel
                self.ataques_normales += 1
                if self.ataques_normales >= self.ataques_para_especial:
                    self.iniciar_especial()
                return a

    def get_asteroides_lanzados(self):
        return [a for a in self.asteroides if not a["attached"] and a["regen"] == 0]

    def draw(self, surface):
        for a in self.asteroides:
            if a["attached"]:
                rot_img = pygame.transform.rotate(a["img"], a["rot"])
                r = rot_img.get_rect(center=(a["x"], a["y"]))
                surface.blit(rot_img, r)
            else:
                rot_img = pygame.transform.rotate(a["img"], a["rot"])
                r = rot_img.get_rect(center=(a["x"], a["y"]))
                surface.blit(rot_img, r)

        br = self.body.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(self.body, br)

        dr = self.dome.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(self.dome, dr)

        nr = self.nucleus_img.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(self.nucleus_img, nr)

        if self.inmune:
            for r, c1, c2 in [(56, (80, 80, 160), (120, 120, 200)),
                              (52, (120, 120, 200), (160, 160, 230)),
                              (48, (160, 160, 230), (200, 200, 240))]:
                t = pygame.time.get_ticks() // 80
                pulso = (t % 6) - 2
                pygame.draw.circle(surface, c1, (int(self.pos.x), int(self.pos.y)),
                                   r + pulso, 2)
                pygame.draw.circle(surface, c2, (int(self.pos.x), int(self.pos.y)),
                                   r + pulso - 2, 1)

        if self.estado == "charging":
            t2 = pygame.time.get_ticks() // 80
            for i in range(3):
                r2 = 50 + i * 10 + (t2 % 8)
                a2 = 200 - i * 60
                pygame.draw.circle(surface, (180, 100, 255, a2),
                                   (int(self.pos.x), int(self.pos.y)), r2, 2)

        if self.estado == "pulling":
            for i in range(6):
                r_pull = 40 + int(self.t * 0.5 + i * 30) % 180
                pygame.draw.circle(surface, (100, 60, 180),
                                   (int(self.pos.x), int(self.pos.y)), r_pull, 1)

        if self.onda_activa:
            alpha = max(0, 200 - self.radio_onda * 2)
            pygame.draw.circle(surface, (140, 60, 200),
                               (int(self.onda_centro.x), int(self.onda_centro.y)),
                               int(self.radio_onda), 3)
            pygame.draw.circle(surface, (200, 120, 255),
                               (int(self.onda_centro.x), int(self.onda_centro.y)),
                               int(self.radio_onda) - 6, 1)

        if self.vulnerable:
            t3 = pygame.time.get_ticks() // 100
            if t3 % 2 == 0:
                pygame.draw.circle(surface, (255, 255, 100),
                                   (int(self.pos.x), int(self.pos.y)), 40, 2)
