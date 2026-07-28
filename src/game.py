import pygame
import sys
import random
from src.config import ANCHO, ALTO, FPS, TITULO, BLANCO, ROJO, AMARILLO, VERDE
from src.background import Background
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy
from src.explosion import Explosion
from src.powerup import PowerUp
from src.boss import Boss


class Game:

    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        self.game_over = False
        self.puntuacion = 0

        self.fondo = Background()
        self.jugador = Player()
        self.balas = []
        self.enemigos = []
        self.explosiones = []
        self.powerups = []

        self.ultima_aparicion = 0
        self.intervalo_aparicion = 1500
        self.ultimo_danio_rayo = 0

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

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            if evento.type == pygame.KEYDOWN:
                if self.game_over and evento.key == pygame.K_SPACE:
                    self.reiniciar()

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

    def update(self):
        ahora = pygame.time.get_ticks()
        if self.game_over:
            return

        teclas = pygame.key.get_pressed()
        self.jugador.update(teclas, ahora)

        # --- DISPARO DEL JUGADOR ---
        if self.jugador.disparar(ahora):
            cx = self.jugador.rect.centerx
            ty = self.jugador.rect.top
            if self.jugador.poder_activo:
                self.balas.append(Bullet(cx, ty - 10))
                self.balas.append(Bullet(cx - 12, ty - 5))
                self.balas.append(Bullet(cx + 12, ty - 5))
            else:
                self.balas.append(Bullet(cx, ty - 10))

        # --- SPAWN DE JEFE ---
        if self.jefe is None and self.puntuacion >= self.proximo_jefe and not self.game_over:
            self.jefe_nivel += 1
            self.proximo_jefe += 5000
            self.jefe = Boss(self.jefe_nivel)
            self.timer_alerta = 90  # 1.5 segundos
            self.enemigos.clear()
            self.balas.clear()

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
            self.jefe.update(self.jugador.rect.centerx, ahora)
            if self.jefe.debe_disparar(ahora):
                cx = self.jefe.rect.centerx
                by = self.jefe.rect.bottom + 5
                self.balas.append(Bullet(cx, by, 5))
                self.balas.append(Bullet(cx - 20, by, 5))
                self.balas.append(Bullet(cx + 20, by, 5))

        rect_jugador = self.jugador.get_rect()

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
                        bala.activa = False
                        impacto = True
                        break
                if not impacto and self.jefe and self.jefe.en_posicion and not self.jefe.inmune:
                    if bala.get_rect().colliderect(self.jefe.get_rect()):
                        self.jefe.vida -= 5
                        bala.activa = False
                        if self.jefe.vida <= 0:
                            self.jefe.activo = False
            else:  # del enemigo
                if bala.get_rect().colliderect(rect_jugador):
                    self.jugador.vida -= 10
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
                self.spawn_powerup(enemigo.rect.centerx, enemigo.rect.centery)

        # --- JEFE CHOCA CON JUGADOR ---
        if self.jefe and self.jefe.en_posicion:
            if self.jefe.get_rect().colliderect(rect_jugador):
                self.jugador.vida -= 30

        # --- RAYO DEL JEFE DAÑA AL JUGADOR ---
        if self.jefe:
            beam_rect = self.jefe.get_beam_rect()
            if beam_rect and beam_rect.colliderect(rect_jugador):
                if ahora - self.ultimo_danio_rayo >= 500:
                    self.jugador.vida -= 15
                    self.ultimo_danio_rayo = ahora

        # --- MUERTE DEL JEFE ---
        if self.jefe and not self.jefe.activo:
            cx, cy = self.jefe.rect.centerx, self.jefe.rect.centery
            self.explosiones.append(Explosion(cx, cy))
            self.explosiones.append(Explosion(cx - 30, cy - 20))
            self.explosiones.append(Explosion(cx + 30, cy - 20))
            self.explosiones.append(Explosion(cx - 20, cy + 15))
            self.explosiones.append(Explosion(cx + 20, cy + 15))
            self.puntuacion += 1000 * self.jefe_nivel
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
                self.powerups.remove(pu)

        # --- EXPLOSIONES ---
        for exp in self.explosiones[:]:
            exp.update()
            if not exp.activa:
                self.explosiones.remove(exp)

        if self.jugador.vida <= 0:
            self.game_over = True

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
        if self.jefe:
            self.jefe.draw(self.pantalla)
        for enemigo in self.enemigos:
            enemigo.draw(self.pantalla)
        for bala in self.balas:
            bala.draw(self.pantalla)
        for pu in self.powerups:
            pu.draw(self.pantalla)
        for exp in self.explosiones:
            exp.draw(self.pantalla)
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
