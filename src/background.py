"""Fondo con efecto de scroll vertical (estrellas que caen)."""

import pygame
import random
from src.config import ANCHO, ALTO, AZUL_OSCURO, BLANCO


class Background:
    """Fondo animado con estrellas que se desplazan hacia abajo,
    simulando que el avion avanza hacia arriba."""

    def __init__(self):
        # Cada estrella es una lista [x, y, velocidad]
        self.estrellas = []
        self._generar_estrellas()

    def _generar_estrellas(self):
        """Crea 100 estrellas en posiciones aleatorias por toda la pantalla."""
        for _ in range(100):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            velocidad = random.uniform(0.5, 2.5)
            self.estrellas.append([x, y, velocidad])

    def update(self):
        """Mueve cada estrella hacia abajo.
        Si sale de la pantalla, reaparece arriba con nueva posicion X."""
        for estrella in self.estrellas:
            estrella[1] += estrella[2]       # avanza en Y
            if estrella[1] > ALTO:           # salio por abajo
                estrella[1] = 0              # reaparece arriba
                estrella[0] = random.randint(0, ANCHO)

    def draw(self, pantalla):
        """Pinta el fondo: color solido + circulos blancos (estrellas)."""
        pantalla.fill(AZUL_OSCURO)
        for estrella in self.estrellas:
            pygame.draw.circle(
                pantalla, BLANCO,
                (int(estrella[0]), int(estrella[1])),
                1  # radio de 1 pixel
            )
