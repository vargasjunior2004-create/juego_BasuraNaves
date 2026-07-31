# Sky Warriors

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
- **6 jefes** en rotación cada 5000 puntos
- Dificultad progresiva
- Sistema de vida con barra de salud
- Puntuación y pantalla de Game Over
- Sprites pixel art (Kenney Asset Pack + Alien UFO Pack)
- **Sonidos procedurales** generados con `wave` y `struct`
- **6 habilidades especiales** que se aprenden al derrotar a cada jefe

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

| Tecla     | Acción           |
|-----------|------------------|
| ← / A     | Mover izquierda  |
| → / D     | Mover derecha    |
| ↑ / W     | Mover arriba     |
| ↓ / S     | Mover abajo      |
| E         | Habilidad 1: Rayo |
| B         | Habilidad 2: Bomba guiada |
| R         | Habilidad 3: Naves aliadas |
| C         | Habilidad 4: Colapso gravitacional |
| X         | Habilidad 5: Misiles inteligentes |
| V         | Habilidad 6: Teletransporte |
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

### Jefes (rotación cada 5000 pts)
1. **Boss** — Nave roja, ráfaga triple + rayo de plasma
2. **Boss2** — Bólido de fuego, disparo en abanico + bola de energía
3. **Boss3** — Comandante alienígena, ráfaga burst + invoca **5 drones** y despliega un **escudo de energía** que reduce el daño a la mitad hasta eliminar todos los drones
4. **Boss4** — Alien rosado, dispara **misiles inteligentes** que persiguen al jugador unos segundos antes de explotar (hay que esquivarlos)
5. **Gravion** — Entidad gravitacional, asteroides orbitales + colapso gravitacional
6. **Boss6** — Alien amarillo, **lluvia de disparos** + **teletransporte** que lo lleva detrás o cerca del jugador (obliga a moverse)

### Habilidades del jugador
Se obtienen al derrotar a cada jefe (el jugador aprende la habilidad especial del jefe vencido). Se recargan cada 2000 puntos.

| Tecla | Habilidad             | Efecto |
|-------|-----------------------|--------|
| E     | Rayo                  | Barrera continua que destruye enemigos al contacto |
| B     | Bomba guiada          | Proyectil teledirigido que persigue al enemigo más cercano |
| R     | Naves aliadas         | Spawnea 2-3 naves kamikaze que persiguen y chocan contra enemigos |
| C     | Colapso gravitacional | Singularidad que atrae a los enemigos y los destruye con una onda expansiva |
| X     | Misiles inteligentes  | Dispara misiles que persiguen al enemigo más cercano y explotan |
| V     | Teletransporte        | Teleport a una posición aleatoria con invulnerabilidad de 1.5 s |

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
│   ├── PNG/Sprites/           # Sprites del Kenney Pack
│   │   ├── Ships/             # Naves (jugador, enemigos, jefe)
│   │   ├── Missiles/          # Balas
│   │   ├── Effects/           # Explosiones
│   │   └── ...                # Otros sprites del pack
│   ├── alien-ufo-pack/        # Sprites del Alien UFO Pack
│   ├── Gravion/               # Sprites PNG del jefe Gravion
│   ├── sounds/                # Efectos de sonido (generados)
│   └── License.txt            # Licencia CC0 de Kenney
├── src/
│   ├── __init__.py
│   ├── config.py              # Constantes del juego
│   ├── game.py                # Bucle principal y HUD
│   ├── background.py          # Fondo con estrellas
│   ├── player.py              # Jugador
│   ├── enemy.py               # Enemigos
│   ├── bullet.py              # Balas
│   ├── explosion.py           # Animación de explosión
│   ├── powerup.py             # Power-ups
│   ├── boss.py                # Jefe 1
│   ├── boss2.py               # Jefe 2 (bólido)
│   ├── boss3.py               # Jefe 3 (alien commander + escudo)
│   ├── boss4.py               # Jefe 4 (alien misiles inteligentes)
│   ├── gravion.py             # Jefe 5 (Gravion)
│   ├── boss6.py               # Jefe 6 (alien teletransporte)
│   ├── drone.py               # Dron auxiliar (AlienDrone)
│   ├── misil.py               # Misil inteligente (homing)
│   ├── energy_ball.py         # Bola de energía (Boss2)
│   └── sonidos.py             # Generación de sonidos WAV
├── main.py                    # Punto de entrada
├── environment.yml            # Dependencias Conda
├── README.md
└── .gitignore
```

---

## Tecnologías

- **Lenguaje:** Python 3.11
- **Framework:** Pygame 2.6.1
- **Sprites:** [Kenney Space Shooter Extension](https://kenney.nl/assets/space-shooter-extension) (CC0) + [Alien UFO Pack](https://kenney.nl/assets/alien-ufo-pack) (CC0)
- **Sonidos:** Generados proceduralmente con `wave` + `struct`
- **Entorno:** Miniconda

---

## Créditos

- Sprites por **Kenney Vleugels** ([Kenney.nl](https://kenney.nl)) — licencia CC0
- Idea y código: proyecto académico

---

## Mejoras futuras

- [ ] Menú principal y pantalla de pausa
- [ ] Guardado de puntuación máxima
- [ ] Modo contrarreloj / endless
