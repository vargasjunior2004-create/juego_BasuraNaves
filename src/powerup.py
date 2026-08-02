"""Power-ups: mejoras que aparecen al destruir enemigos."""

import pygame
import random
from src.config import ANCHO, ALTO, BLANCO, VERDE, AMARILLO


class PowerUp:
    """Objeto que cae y el jugador puede recoger para obtener una mejora."""

    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo  # "vida", "poder", "puntos"
        self.velocidad = 1.5
        self.activo = True

    def get_rect(self):
        return pygame.Rect(self.x - 14, self.y - 14, 28, 28)

    def update(self):
        self.y += self.velocidad
        if self.y > ALTO + 20:
            self.activo = False

    def draw(self, pantalla):
        """Circulo de color con un icono dentro segun el tipo."""
        # Circulo base
        if self.tipo == "vida":
            color = VERDE
        elif self.tipo == "poder":
            color = AMARILLO
        elif self.tipo == "escudo":
            color = (0, 160, 255)
        else:
            color = (0, 180, 255)

        pygame.draw.circle(pantalla, color, (self.x, self.y), 14)
        pygame.draw.circle(pantalla, BLANCO, (self.x, self.y), 14, 2)

        # Icono interior
        if self.tipo == "vida":
            # Cruz (+)
            pygame.draw.rect(pantalla, BLANCO,
                             (self.x - 3, self.y - 8, 6, 16))
            pygame.draw.rect(pantalla, BLANCO,
                             (self.x - 8, self.y - 3, 16, 6))
        elif self.tipo == "poder":
            # Estrella de 4 puntas
            pygame.draw.polygon(pantalla, BLANCO, [
                (self.x, self.y - 8),
                (self.x + 2, self.y - 2),
                (self.x + 8, self.y),
                (self.x + 2, self.y + 2),
                (self.x, self.y + 8),
                (self.x - 2, self.y + 2),
                (self.x - 8, self.y),
                (self.x - 2, self.y - 2)
            ])
        elif self.tipo == "escudo":
            # Escudo: circulo
            pygame.draw.circle(pantalla, BLANCO, (self.x, self.y), 10, 3)
            pygame.draw.circle(pantalla, BLANCO, (self.x, self.y), 5, 1)
        else:  # puntos
            # Diamante / rombo
            pygame.draw.polygon(pantalla, BLANCO, [
                (self.x, self.y - 8),
                (self.x + 6, self.y),
                (self.x, self.y + 8),
                (self.x - 6, self.y)
            ])
