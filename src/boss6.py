import pygame
import random
from src.config import ANCHO, ALTO


class Boss6:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tipo = 6
        self.habilidad_otorgada = 6

        img = pygame.image.load(
            "assets/alien-ufo-pack/PNG/shipYellow_manned.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(img, (90, 65))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -self.rect.height

        self.vida_maxima = 60 * nivel
        self.vida = self.vida_maxima
        self.velocidad_x = 2
        self.direccion = 1
        self.posicion_batalla_y = 80
        self.ultimo_disparo = 0
        self.cooldown_disparo = 1800
        self.activo = True
        self.en_posicion = False
        self.inmune = True

        # Lluvia de disparos
        self.modo_lluvia = False
        self.disparos_lluvia = 0
        self.cooldown_lluvia = 130

        # Teletransporte
        self.ultimo_teleport = 0
        self.teleport_cooldown = 6000
        self.fase_teleport = ""
        self.timer_teleport = 0
        self.visible = True
        self.destino = (ANCHO // 2, 100)

    def get_rect(self):
        if not self.visible or self.fase_teleport:
            return pygame.Rect(0, 0, 0, 0)
        return self.rect.inflate(-10, -10)

    def get_beam_rect(self):
        return None

    def update(self, jugador_x, jugador_y, ahora):
        if not self.en_posicion:
            self.rect.y += 2
            if self.rect.y >= self.posicion_batalla_y:
                self.rect.y = self.posicion_batalla_y
                self.en_posicion = True
            return

        if self.fase_teleport:
            self.timer_teleport -= 1
            if self.fase_teleport == "desapareciendo":
                if self.timer_teleport <= 0:
                    self.fase_teleport = "oculto"
                    self.timer_teleport = 25
                    self.visible = False
            elif self.fase_teleport == "oculto":
                if self.timer_teleport <= 0:
                    self.rect.center = self.destino
                    self.fase_teleport = "apareciendo"
                    self.timer_teleport = 30
                    self.visible = True
            elif self.fase_teleport == "apareciendo":
                if self.timer_teleport <= 0:
                    self.fase_teleport = ""
                    self.iniciar_lluvia(ahora)
            return

        self.rect.x += self.velocidad_x * self.direccion
        if self.rect.right >= ANCHO - 20:
            self.direccion = -1
        elif self.rect.left <= 20:
            self.direccion = 1

        if ahora - self.ultimo_teleport >= self.teleport_cooldown:
            self.iniciar_teleport(ahora, jugador_x, jugador_y)

    def iniciar_teleport(self, ahora, jugador_x, jugador_y):
        self.ultimo_teleport = ahora
        self.fase_teleport = "desapareciendo"
        self.timer_teleport = 40
        self.visible = True
        lado = random.choice(["atras", "lado", "arriba"])
        if lado == "atras":
            dx = random.randint(-80, 80)
            self.destino = (jugador_x + dx, jugador_y + random.randint(90, 140))
        elif lado == "lado":
            signo = 1 if random.random() < 0.5 else -1
            self.destino = (jugador_x + signo * random.randint(120, 180),
                            jugador_y - random.randint(20, 80))
        else:
            self.destino = (jugador_x + random.randint(-60, 60),
                            jugador_y - random.randint(120, 180))
        self.destino = (max(30, min(ANCHO - 30, self.destino[0])),
                        max(40, min(ALTO - 80, self.destino[1])))

    def iniciar_lluvia(self, ahora):
        self.modo_lluvia = True
        self.disparos_lluvia = 14
        self.cooldown_lluvia = 130
        self.ultimo_disparo = ahora

    def debe_disparar(self, ahora):
        if not self.activo or not self.en_posicion:
            return False
        if self.fase_teleport:
            return False
        if self.modo_lluvia:
            if ahora - self.ultimo_disparo >= self.cooldown_lluvia:
                self.ultimo_disparo = ahora
                self.disparos_lluvia -= 1
                if self.disparos_lluvia <= 0:
                    self.modo_lluvia = False
                return True
            return False
        if ahora - self.ultimo_disparo >= self.cooldown_disparo:
            self.ultimo_disparo = ahora
            self.modo_lluvia = True
            self.disparos_lluvia = 10
            self.cooldown_lluvia = 130
            self.ultimo_disparo = ahora
            return True
        return False

    def draw(self, pantalla):
        if not self.visible:
            return
        pantalla.blit(self.image, self.rect)

        if self.fase_teleport:
            t = pygame.time.get_ticks() // 60
            if t % 2 == 0:
                radio = 52
                pygame.draw.circle(pantalla, (255, 230, 120),
                                   self.rect.center, radio, 2)
                pygame.draw.circle(pantalla, (255, 245, 180),
                                   self.rect.center, radio - 6, 1)
        elif self.inmune:
            t = pygame.time.get_ticks() // 80
            pulso = (t % 6) - 2
            radio = 52 + pulso
            pygame.draw.circle(pantalla, (255, 220, 90),
                               self.rect.center, radio + 6, 2)
            pygame.draw.circle(pantalla, (255, 235, 150),
                               self.rect.center, radio, 2)
            pygame.draw.circle(pantalla, (255, 250, 210),
                               self.rect.center, radio - 4, 1)
