# Sky Warriors ✈️

**Shoot 'em up vertical 2D** desarrollado en Python con Pygame.

Proyecto académico de la carrera **Técnico Superior en Sistemas Informáticos** (Bolivia).

---

## Capturas

*(pendiente)*

---

## Características

- Scroll vertical continuo con fondo estrellado
- Avión del jugador controlado por teclado (flechas / WASD)
- Disparo automático con cooldown fijo
- Enemigos que descienden y disparan
- Power-ups: vida extra, triple disparo, puntos bonus
- Jefes cada 5000 puntos con ataque especial (rayo de plasma)
- Dificultad progresiva
- Sistema de vida con barra de salud
- Puntuación y pantalla de Game Over
- Sprites pixel art (Kenney Asset Pack)

---

## Requisitos

- [Miniconda](https://docs.anaconda.com/miniconda/) o [Anaconda](https://www.anaconda.com/)
- Python 3.11+
- Pygame 2.6.1

---

## Instalación

```bash
# 1. Crear el entorno Conda
conda env create -f environment.yml

# 2. Activar el entorno
conda activate juegoAvion

# 3. Ejecutar el juego
python main.py
```

---

## Controles

| Tecla     | Acción         |
|-----------|----------------|
| ← / A     | Mover izquierda |
| → / D     | Mover derecha   |
| ↑ / W     | Mover arriba    |
| ↓ / S     | Mover abajo     |
| ESPACIO   | Reiniciar (Game Over) |

El disparo es **automático** — no necesita botón.

---

## Mecánicas

### Jugador
- **Vida:** 100 HP
- **Disparo:** cada 250 ms
- **Triple disparo:** power-up amarillo (8 segundos)

### Enemigos
- Aparecen desde arriba
- Velocidad y cadencia de disparo variables
- Dificultad aumenta con la puntuación

### Jefe
- Aparece cada **5000 puntos**
- 20 HP × nivel del jefe
- Escudo protector los primeros 1.5 segundos
- Ataques: ráfaga triple + rayo de plasma (cada 4 ataques)
- Durante el rayo, el jefe sigue al jugador

### Power-ups
| Tipo  | Color   | Efecto              |
|-------|---------|---------------------|
| Vida  | Verde   | +30 HP              |
| Poder | Amarillo| Triple disparo 8s   |
| Puntos| Azul    | +200 puntos         |

---

## Estructura del proyecto

```
juegoAvion_pyton/
├── assets/
│   ├── PNG/Sprites/       # Sprites del Kenney Pack
│   │   ├── Ships/         # Naves (jugador, enemigos, jefe)
│   │   ├── Missiles/      # Balas
│   │   ├── Effects/       # Explosiones
│   │   └── ...            # Otros sprites del pack
│   └── License.txt        # Licencia CC0 de Kenney
├── src/
│   ├── __init__.py
│   ├── config.py          # Constantes del juego
│   ├── game.py            # Bucle principal y HUD
│   ├── background.py      # Fondo con estrellas
│   ├── player.py          # Jugador
│   ├── enemy.py           # Enemigos
│   ├── bullet.py          # Balas
│   ├── explosion.py       # Animación de explosión
│   ├── powerup.py         # Power-ups
│   └── boss.py            # Jefe y ataque especial
├── main.py                # Punto de entrada
├── environment.yml        # Dependencias Conda
├── README.md
└── .gitignore
```

---

## Tecnologías

- **Lenguaje:** Python 3.11
- **Framework:** Pygame 2.6.1
- **Sprites:** [Kenney Space Shooter Extension](https://kenney.nl/assets/space-shooter-extension) (CC0)
- **Entorno:** Miniconda

---

## Créditos

- Sprites por **Kenney Vleugels** ([Kenney.nl](https://kenney.nl)) — licencia CC0
- Idea y código: proyecto académico

---

## Mejoras futuras

- [ ] Efectos de sonido y música
- [ ] Más tipos de enemigos
- [ ] Jefes con patrones adicionales
- [ ] Menú principal y pantalla de pausa
- [ ] Guardado de puntuación máxima
- [ ] Modo contrarreloj / endless
