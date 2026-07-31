import pygame
import sys
import random
import math
from src.config import ANCHO, ALTO, FPS, TITULO, BLANCO, ROJO, AMARILLO, VERDE
from src.background import Background
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy
from src.explosion import Explosion
from src.powerup import PowerUp
from src.boss import Boss
from src.boss2 import Boss2
from src.boss3 import Boss3
from src.gravion import Gravion
from src.drone import AlienDrone
from src.energy_ball import EnergyBall
from src.sonidos import GestorSonidos
from src.explosion import AreaExplosion


class Game:

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.game_over = False
        self.puntuacion = 0

        self.sonidos = GestorSonidos()
        self.fondo = Background()
        self.jugador = Player()
        self.balas = []
        self.enemigos = []
        self.explosiones = []
        self.powerups = []

        self.ultima_aparicion = 0
        self.intervalo_aparicion = 1500
        self.ultimo_danio_rayo = 0
        self.ultimo_danio_aoe = 0
        self.areas_explosion = []
        self.drones = []

        self.habilidad_1_tiene = False
        self.habilidad_1_lista = False
        self.habilidad_1_puntos_base = 0
        self.habilidad_2_tiene = False
        self.habilidad_2_lista = False
        self.habilidad_2_puntos_base = 0
        self.habilidad_3_tiene = False
        self.habilidad_3_lista = False
        self.habilidad_3_puntos_base = 0
        self.ultimo_danio_habilidad = 0
        self.ultimo_disparo_habilidad = 0
        self.habilidad_projectiles = []
        self.habilidad_explosiones = []
        self.habilidad_aliados = []
        self.img_ally = pygame.transform.scale(
            pygame.image.load(
                "assets/PNG/Sprites/Ships/spaceShips_001.png").convert_alpha(),
            (16, 16))

        # Jefe
        self.jefe = None
        self.jefe_nivel = 0
        self.proximo_jefe = 5000
        self.timer_alerta = 0  # frames que muestra "¡JEFE!"

    def get_dificultad(self):
        return self.puntuacion // 2000

    def reiniciar(self):
        self.jugador = Player()
        self.balas.clear()
        self.enemigos.clear()
        self.explosiones.clear()
        self.powerups.clear()
        self.puntuacion = 0
        self.game_over = False
        self.jefe = None
        self.jefe_nivel = 0
        self.proximo_jefe = 5000
        self.timer_alerta = 0
        self.ultima_aparicion = 0
        self.areas_explosion.clear()
        self.ultimo_danio_aoe = 0
        self.habilidad_1_tiene = False
        self.habilidad_1_lista = False
        self.habilidad_1_puntos_base = 0
        self.habilidad_2_tiene = False
        self.habilidad_2_lista = False
        self.habilidad_2_puntos_base = 0
        self.habilidad_3_tiene = False
        self.habilidad_3_lista = False
        self.habilidad_3_puntos_base = 0
        self.ultimo_danio_habilidad = 0
        self.ultimo_disparo_habilidad = 0
        self.habilidad_projectiles.clear()
        self.habilidad_explosiones.clear()
        self.habilidad_aliados.clear()
        self.drones.clear()

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            if evento.type == pygame.KEYDOWN:
                if self.game_over and evento.key == pygame.K_SPACE:
                    self.reiniciar()
                if evento.key == pygame.K_e and not self.game_over:
                    if (self.habilidad_1_tiene and self.habilidad_1_lista
                            and not self.jugador.habilidad_activa):
                        self.jugador.habilidad_activa = True
                        self.jugador.habilidad_tipo = 1
                        self.jugador.tiempo_habilidad = self.jugador.duracion_habilidad
                        self.habilidad_1_lista = False
                        self.habilidad_1_puntos_base = self.puntuacion
                        self.sonidos.reproducir("habilidad")
                if evento.key == pygame.K_b and not self.game_over:
                    if (self.habilidad_2_tiene and self.habilidad_2_lista
                            and not self.jugador.habilidad_activa):
                        self.jugador.habilidad_activa = True
                        self.jugador.habilidad_tipo = 2
                        self.jugador.tiempo_habilidad = self.jugador.duracion_habilidad
                        self.habilidad_2_lista = False
                        self.habilidad_2_puntos_base = self.puntuacion
                        self.sonidos.reproducir("habilidad")
                if evento.key == pygame.K_r and not self.game_over:
                    if (self.habilidad_3_tiene and self.habilidad_3_lista
                            and not self.jugador.habilidad_activa):
                        self.jugador.habilidad_activa = True
                        self.jugador.habilidad_tipo = 3
                        self.jugador.tiempo_habilidad = self.jugador.duracion_habilidad
                        self.habilidad_3_lista = False
                        self.habilidad_3_puntos_base = self.puntuacion
                        self.sonidos.reproducir("habilidad")

    def spawn_powerup(self, x, y):
        if random.random() < 0.15:
            r = random.randint(1, 10)
            if r <= 4:
                tipo = "vida"
            elif r <= 7:
                tipo = "poder"
            else:
                tipo = "puntos"
            self.powerups.append(PowerUp(x, y, tipo))

    def _aplicar_danio_jefe(self, danio):
        if not self.jefe:
            return
        if hasattr(self.jefe, "recibir_danio"):
            self.jefe.recibir_danio(danio)
        else:
            self.jefe.vida -= danio
            if self.jefe.vida <= 0:
                self.jefe.activo = False

    def _chequear_escudo_jefe(self):
        if (self.jefe and self.jefe.tipo == 3
                and getattr(self.jefe, "escudo_activo", False)
                and not self.drones):
            self.jefe.desactivar_escudo()

    def update(self):
        ahora = pygame.time.get_ticks()
        if self.game_over:
            return

        teclas = pygame.key.get_pressed()
        self.jugador.update(teclas, ahora)

        # --- DISPARO DEL JUGADOR ---
        if not self.jugador.habilidad_activa:
            if self.jugador.disparar(ahora):
                cx = self.jugador.rect.centerx
                ty = self.jugador.rect.top
                if self.jugador.poder_activo:
                    self.balas.append(Bullet(cx, ty - 10))
                    self.balas.append(Bullet(cx - 12, ty - 5))
                    self.balas.append(Bullet(cx + 12, ty - 5))
                else:
                    self.balas.append(Bullet(cx, ty - 10))
                self.sonidos.reproducir("disparo")

        # --- SPAWN DE JEFE ---
        if self.jefe is None and self.puntuacion >= self.proximo_jefe and not self.game_over:
            self.jefe_nivel += 1
            self.proximo_jefe += 5000
            if self.jefe_nivel % 4 == 0:
                self.jefe = Gravion(self.jefe_nivel)
            elif self.jefe_nivel % 4 == 3:
                self.jefe = Boss3(self.jefe_nivel)
            elif self.jefe_nivel % 4 == 2:
                self.jefe = Boss2(self.jefe_nivel)
            else:
                self.jefe = Boss(self.jefe_nivel)
            self.timer_alerta = 90  # 1.5 segundos
            self.enemigos.clear()
            self.balas.clear()
            self.sonidos.reproducir("alarma_jefe")

        if self.timer_alerta > 0:
            self.timer_alerta -= 1
            if self.timer_alerta == 0 and self.jefe:
                self.jefe.inmune = False  # el escudo se desactiva

        # --- SPAWN DE ENEMIGOS (solo si no hay jefe) ---
        if self.jefe is None:
            diff = self.get_dificultad()
            intervalo = max(400, self.intervalo_aparicion - diff * 100)
            if ahora - self.ultima_aparicion >= intervalo:
                vel_extra = diff * 0.3
                e = Enemy()
                e.velocidad = random.uniform(1.5, 3.5) + vel_extra
                self.enemigos.append(e)
                self.ultima_aparicion = ahora

        # --- ENEMIGOS ---
        for enemigo in self.enemigos[:]:
            enemigo.update()
            if enemigo.debe_disparar(ahora):
                self.balas.append(
                    Bullet(enemigo.rect.centerx, enemigo.rect.bottom + 5, 5)
                )
            if not enemigo.activo:
                self.enemigos.remove(enemigo)

        # --- JEFE ---
        if self.jefe:
            if self.jefe.tipo != 4:
                self.jefe.update(self.jugador.rect.centerx, ahora)
            if self.jefe.tipo == 1:
                if self.jefe.debe_disparar(ahora):
                    cx = self.jefe.rect.centerx
                    by = self.jefe.rect.bottom + 5
                    self.balas.append(Bullet(cx, by, 5))
                    self.balas.append(Bullet(cx - 20, by, 5))
                    self.balas.append(Bullet(cx + 20, by, 5))
                    self.sonidos.reproducir("jefe_disparo")
            elif self.jefe.tipo == 2:
                if self.jefe.debe_disparar(ahora):
                    if self.jefe.es_disparo_especial:
                        self.jefe.es_disparo_especial = False
                        ball = EnergyBall(
                            self.jefe.rect.centerx, self.jefe.rect.bottom + 5,
                            self.jugador.rect.centerx, self.jefe.nivel)
                        self.jefe.energy_balls.append(ball)
                        self.sonidos.reproducir("bomba")
                    else:
                        self.balas.append(
                            Bullet(self.jefe.rect.centerx, self.jefe.rect.bottom + 5, 5))
                        self.sonidos.reproducir("jefe_disparo")
            elif self.jefe.tipo == 3:
                if self.jefe.debe_disparar(ahora):
                    self.balas.append(
                        Bullet(self.jefe.rect.centerx, self.jefe.rect.bottom + 5, 5))
                    self.sonidos.reproducir("rafaga")
                if self.jefe.refuerzos_pendientes:
                    self.jefe.refuerzos_pendientes = False
                    self.jefe.activar_escudo()
                    self.sonidos.reproducir("alarma_jefe")
                    for _ in range(5):
                        x = random.randint(30, ANCHO - 30)
                        y = random.randint(-50, -20)
                        self.drones.append(
                            AlienDrone(x, y,
                                       self.jugador.rect.centerx,
                                       self.jugador.rect.centery))
            elif self.jefe.tipo == 4:
                player_vec = (self.jugador.rect.centerx, self.jugador.rect.centery)
                self.jefe.update(ahora, player_vec)
                if self.jefe.debe_disparar(ahora):
                    self.jefe.lanzar_asteroide(player_vec)
                    self.sonidos.reproducir("jefe_disparo")

        rect_jugador = self.jugador.get_rect()

        # --- GRAVION: ASTERIODES LANZADOS ---
        if self.jefe and self.jefe.tipo == 4:
            for a in self.jefe.get_asteroides_lanzados():
                r = pygame.Rect(a["x"] - 14, a["y"] - 14, 28, 28)
                if r.colliderect(rect_jugador):
                    self.jugador.vida -= 15
                    a["regen"] = 180
                    self.explosiones.append(Explosion(int(a["x"]), int(a["y"])))

        # --- GRAVION: ATRACCION ---
        if self.jefe and self.jefe.tipo == 4 and self.jefe.atraccion_activa:
            dx = self.jefe.pos.x - self.jugador.rect.centerx
            dy = self.jefe.pos.y - self.jugador.rect.centery
            d = math.hypot(dx, dy)
            if d > 10:
                fuerza = self.jefe.fuerza_atraccion
                self.jugador.rect.x += dx / d * fuerza
                self.jugador.rect.y += dy / d * fuerza

        # --- GRAVION: ONDA EXPANSIVA ---
        if self.jefe and self.jefe.tipo == 4 and self.jefe.onda_activa:
            dx = self.jugador.rect.centerx - self.jefe.onda_centro.x
            dy = self.jugador.rect.centery - self.jefe.onda_centro.y
            d = math.hypot(dx, dy)
            if abs(d - self.jefe.radio_onda) < 20:
                self.jugador.vida -= 10
            if d < self.jefe.radio_onda + 20 and d > 0:
                self.jugador.rect.x += dx / d * 8
                self.jugador.rect.y += dy / d * 8

        # --- BALAS Y COLISIONES ---
        for bala in self.balas[:]:
            bala.update()
            if not bala.activa:
                self.balas.remove(bala)
                continue

            if bala.velocidad < 0:  # del jugador
                impacto = False
                for enemigo in self.enemigos[:]:
                    if bala.get_rect().colliderect(enemigo.get_rect()):
                        self.explosiones.append(
                            Explosion(enemigo.rect.centerx, enemigo.rect.centery)
                        )
                        self.enemigos.remove(enemigo)
                        self.puntuacion += 100
                        self.spawn_powerup(enemigo.rect.centerx, enemigo.rect.centery)
                        self.sonidos.reproducir("explosion")
                        bala.activa = False
                        impacto = True
                        break
                if not impacto:
                    for drone in self.drones[:]:
                        if bala.get_rect().colliderect(drone.get_rect()):
                            drone.vida -= 5
                            bala.activa = False
                            if drone.vida <= 0:
                                self.explosiones.append(
                                    Explosion(int(drone.x), int(drone.y)))
                                self.drones.remove(drone)
                                self.puntuacion += 50
                                self.spawn_powerup(int(drone.x), int(drone.y))
                                self.sonidos.reproducir("explosion")
                            impacto = True
                            break
                if not impacto and self.jefe and self.jefe.en_posicion and not self.jefe.inmune:
                    if bala.get_rect().colliderect(self.jefe.get_rect()):
                        danio = 5
                        if self.jefe.tipo == 4 and hasattr(self.jefe, 'vulnerable') and self.jefe.vulnerable:
                            danio = 20
                        self._aplicar_danio_jefe(danio)
                        bala.activa = False
            else:  # del enemigo
                if bala.get_rect().colliderect(rect_jugador):
                    self.jugador.vida -= 10
                    self.sonidos.reproducir("golpe")
                    bala.activa = False

            if not bala.activa:
                self.balas.remove(bala)

        # --- ENEMIGO CHOCA CON JUGADOR ---
        for enemigo in self.enemigos[:]:
            if enemigo.get_rect().colliderect(rect_jugador):
                self.explosiones.append(
                    Explosion(enemigo.rect.centerx, enemigo.rect.centery)
                )
                self.enemigos.remove(enemigo)
                self.jugador.vida -= 20
                self.sonidos.reproducir("golpe")
                self.spawn_powerup(enemigo.rect.centerx, enemigo.rect.centery)

        # --- DRONES ---
        for drone in self.drones[:]:
            drone.update(self.jugador.rect.centerx, self.jugador.rect.centery)
            if drone.get_rect().colliderect(rect_jugador):
                self.explosiones.append(Explosion(int(drone.x), int(drone.y)))
                self.drones.remove(drone)
                self.jugador.vida -= 10
            elif not drone.activo:
                self.drones.remove(drone)

        self._chequear_escudo_jefe()

        # --- JEFE CHOCA CON JUGADOR ---
        if self.jefe and self.jefe.en_posicion:
            if self.jefe.get_rect().colliderect(rect_jugador):
                self.jugador.vida -= 30

        # --- ENERGY BALLS (BOSS2) ---
        if self.jefe and self.jefe.tipo == 2:
            for ball in self.jefe.energy_balls[:]:
                ball.update(self.jugador.rect.centery)
                if ball.debe_explotar():
                    self.areas_explosion.append(
                        AreaExplosion(ball.x, ball.y, 15 * self.jefe.nivel))
                if not ball.activa:
                    self.jefe.energy_balls.remove(ball)

        # --- AREA EXPLOSIONS ---
        for ae in self.areas_explosion[:]:
            ae.update()
            if ae.get_rect().colliderect(rect_jugador):
                if ahora - self.ultimo_danio_aoe >= 500:
                    self.jugador.vida -= ae.danio
                    self.ultimo_danio_aoe = ahora
            if not ae.activa:
                self.areas_explosion.remove(ae)

        # --- RAYO DEL JEFE DAÑA AL JUGADOR ---
        if self.jefe:
            beam_rect = self.jefe.get_beam_rect()
            if beam_rect and beam_rect.colliderect(rect_jugador):
                if ahora - self.ultimo_danio_rayo >= 500:
                    self.jugador.vida -= 15
                    self.ultimo_danio_rayo = ahora

        # --- HABILIDAD DEL JUGADOR ---
        if self.jugador.habilidad_activa:
            self.jugador.tiempo_habilidad -= 1
            if self.jugador.tiempo_habilidad <= 0:
                self.jugador.habilidad_activa = False
                self.jugador.tiempo_habilidad = 0

            if self.jugador.habilidad_tipo == 1:
                beam_rect = self.jugador.get_beam_rect()
                if beam_rect:
                    for enemigo in self.enemigos[:]:
                        if beam_rect.colliderect(enemigo.get_rect()):
                            self.explosiones.append(
                                Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                            self.enemigos.remove(enemigo)
                            self.puntuacion += 100
                    if self.jefe and self.jefe.en_posicion:
                        if beam_rect.colliderect(self.jefe.get_rect()):
                            if ahora - self.ultimo_danio_habilidad >= 500:
                                self._aplicar_danio_jefe(8)
                                self.ultimo_danio_habilidad = ahora

            elif self.jugador.habilidad_tipo == 2:
                if ahora - self.ultimo_disparo_habilidad >= 400:
                    self.ultimo_disparo_habilidad = ahora
                    px = self.jugador.rect.centerx
                    py = self.jugador.rect.top
                    vx, vy = 0, -7
                    if self.enemigos:
                        nearest = min(self.enemigos,
                                      key=lambda e: (e.rect.centerx - px) ** 2
                                      + (e.rect.centery - py) ** 2)
                        dx = nearest.rect.centerx - px
                        d = math.hypot(dx, py - nearest.rect.centery)
                        if d > 0:
                            vx = dx / d * 7
                    self.habilidad_projectiles.append(
                        {"x": px, "y": py, "vx": vx, "vy": vy, "activo": True})
                    self.sonidos.reproducir("bomba")

            elif self.jugador.habilidad_tipo == 3:
                if not self.habilidad_aliados:
                    for _ in range(random.randint(2, 3)):
                        self.habilidad_aliados.append({
                            "x": self.jugador.rect.centerx,
                            "y": self.jugador.rect.top,
                            "vx": 0, "vy": -4,
                            "activo": True,
                        })

        for p in self.habilidad_projectiles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -30:
                p["activo"] = False
            if self.enemigos:
                nearest = min(self.enemigos,
                              key=lambda e: (e.rect.centerx - p["x"]) ** 2
                              + (e.rect.centery - p["y"]) ** 2)
                dx = nearest.rect.centerx - p["x"]
                dy = nearest.rect.centery - p["y"]
                d = math.hypot(dx, dy)
                if d > 0:
                    p["vx"] += (dx / d * 7 - p["vx"]) * 0.15
                    p["vy"] += (dy / d * 7 - p["vy"]) * 0.15
            radio_col = 16
            impacto = False
            for enemigo in self.enemigos[:]:
                r = pygame.Rect(p["x"] - radio_col, p["y"] - radio_col,
                                radio_col * 2, radio_col * 2)
                if r.colliderect(enemigo.get_rect()):
                    self.explosiones.append(
                        Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                    self.enemigos.remove(enemigo)
                    self.puntuacion += 100
                    impacto = True
                    break
            if not impacto and self.jefe and self.jefe.en_posicion:
                r = pygame.Rect(p["x"] - radio_col, p["y"] - radio_col,
                                radio_col * 2, radio_col * 2)
                if r.colliderect(self.jefe.get_rect()):
                    self._aplicar_danio_jefe(15)
                    impacto = True
            if impacto or not p["activo"]:
                self.habilidad_explosiones.append(
                    AreaExplosion(p["x"], p["y"], 10))
                self.habilidad_projectiles.remove(p)

        for ae in self.habilidad_explosiones[:]:
            ae.update()
            for enemigo in self.enemigos[:]:
                if ae.get_rect().colliderect(enemigo.get_rect()):
                    self.explosiones.append(
                        Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                    self.enemigos.remove(enemigo)
                    self.puntuacion += 100
            if self.jefe and self.jefe.en_posicion:
                if ae.get_rect().colliderect(self.jefe.get_rect()):
                    if ahora - self.ultimo_danio_habilidad >= 500:
                        self._aplicar_danio_jefe(ae.danio)
                        self.ultimo_danio_habilidad = ahora
            if not ae.activa:
                self.habilidad_explosiones.remove(ae)

        # --- RECARGA DE HABILIDADES ---
        if not self.habilidad_1_lista and not (self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 1):
            if self.puntuacion - self.habilidad_1_puntos_base >= 2000:
                self.habilidad_1_lista = True
        if not self.habilidad_2_lista and not (self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 2):
            if self.puntuacion - self.habilidad_2_puntos_base >= 2000:
                self.habilidad_2_lista = True
        if not self.habilidad_3_lista and not (self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 3):
            if self.puntuacion - self.habilidad_3_puntos_base >= 2000:
                self.habilidad_3_lista = True

        # --- ALIADOS (HAB 3) ---
        for al in self.habilidad_aliados[:]:
            if not al["activo"]:
                self.habilidad_aliados.remove(al)
                continue
            if not self.jugador.habilidad_activa or self.jugador.habilidad_tipo != 3:
                al["activo"] = False
                self.habilidad_aliados.remove(al)
                continue
            if self.enemigos:
                nearest = min(self.enemigos,
                              key=lambda e: (e.rect.centerx - al["x"]) ** 2
                              + (e.rect.centery - al["y"]) ** 2)
                dx = nearest.rect.centerx - al["x"]
                dy = nearest.rect.centery - al["y"]
                d = math.hypot(dx, dy)
                if d > 0:
                    vel = 4
                    al["vx"] += (dx / d * vel - al["vx"]) * 0.08
                    al["vy"] += (dy / d * vel - al["vy"]) * 0.08
            al["x"] += al["vx"]
            al["y"] += al["vy"]
            impacto = False
            for enemigo in self.enemigos[:]:
                r = pygame.Rect(al["x"] - 8, al["y"] - 8, 16, 16)
                if r.colliderect(enemigo.get_rect()):
                    self.explosiones.append(
                        Explosion(enemigo.rect.centerx, enemigo.rect.centery))
                    self.enemigos.remove(enemigo)
                    self.puntuacion += 50
                    impacto = True
                    break
            if impacto:
                self.explosiones.append(Explosion(int(al["x"]), int(al["y"])))
                al["activo"] = False
            if al["y"] < -30 or al["y"] > ALTO + 30 or al["x"] < -30 or al["x"] > ANCHO + 30:
                al["activo"] = False

        # --- MUERTE DEL JEFE ---
        if self.jefe and not self.jefe.activo:
            cx, cy = self.jefe.rect.centerx, self.jefe.rect.centery
            self.explosiones.append(Explosion(cx, cy))
            self.explosiones.append(Explosion(cx - 30, cy - 20))
            self.explosiones.append(Explosion(cx + 30, cy - 20))
            self.explosiones.append(Explosion(cx - 20, cy + 15))
            self.explosiones.append(Explosion(cx + 20, cy + 15))
            self.puntuacion += 1000 * self.jefe_nivel
            self.sonidos.reproducir("explosion")
            hab = getattr(self.jefe, "habilidad_otorgada", None)
            if hab == 1:
                self.habilidad_1_tiene = True
                self.habilidad_1_lista = True
            elif hab == 2:
                self.habilidad_2_tiene = True
                self.habilidad_2_lista = True
            elif hab == 3:
                self.habilidad_3_tiene = True
                self.habilidad_3_lista = True
            self.jefe = None

        # --- POWER-UPS ---
        for pu in self.powerups[:]:
            pu.update()
            if not pu.activo:
                self.powerups.remove(pu)
                continue
            if pu.get_rect().colliderect(rect_jugador):
                if pu.tipo == "vida":
                    self.jugador.vida = min(
                        self.jugador.vida + 30, self.jugador.vida_maxima
                    )
                elif pu.tipo == "poder":
                    self.jugador.activar_poder()
                else:
                    self.puntuacion += 200
                self.sonidos.reproducir("powerup")
                self.powerups.remove(pu)

        # --- EXPLOSIONES ---
        for exp in self.explosiones[:]:
            exp.update()
            if not exp.activa:
                self.explosiones.remove(exp)

        if self.jugador.vida <= 0:
            self.game_over = True
            self.sonidos.reproducir("game_over")

        self.fondo.update()

    def dibujar_hud(self):
        fuente = pygame.font.Font(None, 36)
        fuente_pequena = pygame.font.Font(None, 20)

        texto_score = fuente.render(f"Puntos: {self.puntuacion}", True, BLANCO)
        self.pantalla.blit(texto_score, (10, 10))

        if self.jugador.poder_activo:
            resto = max(0, (self.jugador.duracion_poder -
                          (pygame.time.get_ticks() - self.jugador.tiempo_inicio_poder)) // 1000)
            texto_poder = fuente_pequena.render(f"PODER {resto}s", True, AMARILLO)
            self.pantalla.blit(texto_poder, (10, 45))

        y_hab = 70
        if self.habilidad_1_tiene:
            if self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 1:
                resto = (self.jugador.tiempo_habilidad + 59) // 60
                texto = fuente_pequena.render(f"E=RAYO {resto}s", True, (0, 200, 255))
            elif self.habilidad_1_lista:
                texto = fuente_pequena.render("E=RAYO [LISTA]", True, VERDE)
            else:
                pct = min(100, (self.puntuacion - self.habilidad_1_puntos_base) * 100 // 2000)
                texto = fuente_pequena.render(f"E=RAYO {pct}%", True, (150, 150, 150))
            self.pantalla.blit(texto, (10, y_hab))
            y_hab += 18

        if self.habilidad_2_tiene:
            if self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 2:
                resto = (self.jugador.tiempo_habilidad + 59) // 60
                texto = fuente_pequena.render(f"B=BOMBA {resto}s", True, (0, 200, 255))
            elif self.habilidad_2_lista:
                texto = fuente_pequena.render("B=BOMBA [LISTA]", True, VERDE)
            else:
                pct = min(100, (self.puntuacion - self.habilidad_2_puntos_base) * 100 // 2000)
                texto = fuente_pequena.render(f"B=BOMBA {pct}%", True, (150, 150, 150))
            self.pantalla.blit(texto, (10, y_hab))
            y_hab += 18

        if self.habilidad_3_tiene:
            if self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 3:
                resto = (self.jugador.tiempo_habilidad + 59) // 60
                texto = fuente_pequena.render(f"R=NAVES {resto}s", True, (0, 200, 255))
            elif self.habilidad_3_lista:
                texto = fuente_pequena.render("R=NAVES [LISTA]", True, VERDE)
            else:
                pct = min(100, (self.puntuacion - self.habilidad_3_puntos_base) * 100 // 2000)
                texto = fuente_pequena.render(f"R=NAVES {pct}%", True, (150, 150, 150))
            self.pantalla.blit(texto, (10, y_hab))
            y_hab += 18

        # Barra de vida del jugador
        ancho_barra = 180
        alto_barra = 18
        x_barra = ANCHO - ancho_barra - 10
        y_barra = 12

        pygame.draw.rect(self.pantalla, (40, 40, 40),
                         (x_barra, y_barra, ancho_barra, alto_barra))
        proporcion = max(0, self.jugador.vida / self.jugador.vida_maxima)
        ancho_vida = int(ancho_barra * proporcion)
        color_vida = (int(255 * (1 - proporcion)),
                      int(255 * proporcion), 0)
        pygame.draw.rect(self.pantalla, color_vida,
                         (x_barra, y_barra, ancho_vida, alto_barra))
        pygame.draw.rect(self.pantalla, BLANCO,
                         (x_barra, y_barra, ancho_barra, alto_barra), 2)

        # Barra de vida del jefe
        if self.jefe:
            ancho_boss = 300
            x_boss = (ANCHO - ancho_boss) // 2
            y_boss = 55
            pygame.draw.rect(self.pantalla, (40, 40, 40),
                             (x_boss, y_boss, ancho_boss, 14))
            prop_boss = max(0, self.jefe.vida / self.jefe.vida_maxima)
            pygame.draw.rect(self.pantalla, (220, 0, 0),
                             (x_boss, y_boss, int(ancho_boss * prop_boss), 14))
            pygame.draw.rect(self.pantalla, BLANCO,
                             (x_boss, y_boss, ancho_boss, 14), 2)
            texto_jefe = fuente_pequena.render(f"JEFE Nvl.{self.jefe.nivel}", True, ROJO)
            self.pantalla.blit(texto_jefe, (x_boss + 5, y_boss - 16))

        # Alerta de jefe
        if self.timer_alerta > 0:
            fuente_alerta = pygame.font.Font(None, 72)
            texto = fuente_alerta.render("¡JEFE!", True, ROJO)
            rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
            self.pantalla.blit(texto, rect)
            texto2 = fuente.render("PREPARATE", True, BLANCO)
            rect2 = texto2.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
            self.pantalla.blit(texto2, rect2)

    def dibujar_game_over(self):
        fuente_grande = pygame.font.Font(None, 64)
        fuente_chica = pygame.font.Font(None, 36)

        texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
        texto_rect = texto_game_over.get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
        self.pantalla.blit(texto_game_over, texto_rect)

        texto_reinicio = fuente_chica.render("Presiona ESPACIO para reiniciar", True, BLANCO)
        texto_reinicio_rect = texto_reinicio.get_rect(center=(ANCHO // 2, ALTO // 2 + 30))
        self.pantalla.blit(texto_reinicio, texto_reinicio_rect)

    def draw(self):
        self.fondo.draw(self.pantalla)
        self.jugador.draw(self.pantalla)
        if self.jugador.habilidad_activa and self.jugador.habilidad_tipo == 1:
            beam_rect = self.jugador.get_beam_rect()
            if beam_rect:
                bw = beam_rect.width
                bx = beam_rect.x
                by = beam_rect.y
                bh = beam_rect.height
                pg = pygame.draw.rect
                pg(self.pantalla, (60, 20, 100, 128), (bx - 8, by, bw + 16, bh))
                pg(self.pantalla, (120, 40, 180), (bx - 3, by, bw + 6, bh))
                pg(self.pantalla, (200, 100, 240), (bx, by, bw, bh))
                pg(self.pantalla, (255, 230, 255), (bx, by + bh - bh // 4, bw, bh // 4))
        if self.jefe:
            self.jefe.draw(self.pantalla)
        for drone in self.drones:
            drone.draw(self.pantalla)
        for enemigo in self.enemigos:
            enemigo.draw(self.pantalla)
        for bala in self.balas:
            bala.draw(self.pantalla)
        for pu in self.powerups:
            pu.draw(self.pantalla)
        for exp in self.explosiones:
            exp.draw(self.pantalla)
        for ae in self.areas_explosion:
            ae.draw(self.pantalla)
        for p in self.habilidad_projectiles:
            cx, cy = int(p["x"]), int(p["y"])
            pygame.draw.circle(self.pantalla, (255, 150, 0), (cx, cy), 14, 2)
            pygame.draw.circle(self.pantalla, (255, 200, 0), (cx, cy), 10, 2)
            pygame.draw.circle(self.pantalla, (255, 255, 200), (cx, cy), 8)
            pygame.draw.circle(self.pantalla, (255, 200, 50), (cx, cy), 4)
        for ae in self.habilidad_explosiones:
            ae.draw(self.pantalla)
        for al in self.habilidad_aliados:
            if al["activo"]:
                r = self.img_ally.get_rect(center=(int(al["x"]), int(al["y"])))
                self.pantalla.blit(self.img_ally, r)
        self.dibujar_hud()
        if self.game_over:
            self.dibujar_game_over()
        pygame.display.flip()

    def ejecutar(self):
        while self.corriendo:
            self.manejar_eventos()
            self.update()
            self.draw()
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()
