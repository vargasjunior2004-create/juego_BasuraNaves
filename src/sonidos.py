import pygame
import wave
import struct
import math
import random
import os

DIR = "assets/sounds"
RATE = 22050

def _generar_wav(nombre, duracion, frecuencia, forma="seno",
                 volumen=0.4, barrido=0, ruido=False):
    os.makedirs(DIR, exist_ok=True)
    ruta = os.path.join(DIR, nombre)
    nframes = int(RATE * duracion)
    datos = bytearray()
    for i in range(nframes):
        t = i / RATE
        v = volumen
        # fade out
        if i > nframes * 0.8:
            v *= 1 - (i - nframes * 0.8) / (nframes * 0.2)
        if forma == "seno":
            f = frecuencia + barrido * t
            muestra = int(v * 32767 * math.sin(2 * math.pi * f * t))
        elif forma == "cuadrada":
            f = frecuencia + barrido * t
            muestra = int(v * 32767 * (1 if math.sin(2 * math.pi * f * t) >= 0 else -1))
        elif forma == "diente":
            f = frecuencia + barrido * t
            fase = (t * f) % 1
            muestra = int(v * 32767 * (2 * fase - 1))
        elif forma == "ruido":
            muestra = int(v * 32767 * random.uniform(-1, 1))
        elif forma == "golpe":
            env = math.exp(-t * 20)
            muestra = int(v * 32767 * env * math.sin(2 * math.pi * frecuencia * t))
        if ruido:
            muestra += int(v * 0.3 * 32767 * random.uniform(-1, 1))
        muestra = max(-32768, min(32767, muestra))
        datos.extend(struct.pack("<h", int(muestra)))

    with wave.open(ruta, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(bytes(datos))


def _generar_todos():
    os.makedirs(DIR, exist_ok=True)
    for nombre, args in [
        ("disparo.wav", (0.08, 900, "cuadrada", 0.25)),
        ("explosion.wav", (0.25, 200, "ruido", 0.35)),
        ("powerup.wav", (0.25, 400, "seno", 0.3, 600)),
        ("golpe.wav", (0.12, 100, "golpe", 0.4)),
        ("alarma_jefe.wav", (0.5, 440, "cuadrada", 0.2, 220)),
        ("habilidad.wav", (0.3, 300, "seno", 0.3, 600)),
        ("game_over.wav", (0.6, 500, "seno", 0.3, -400)),
        ("jefe_disparo.wav", (0.12, 300, "cuadrada", 0.2)),
        ("bomba.wav", (0.2, 200, "diente", 0.25, 300)),
        ("rafaga.wav", (0.06, 600, "cuadrada", 0.15)),
    ]:
        ruta = os.path.join(DIR, nombre)
        if not os.path.exists(ruta):
            try:
                _generar_wav(nombre, *args)
            except PermissionError:
                pass


class GestorSonidos:

    def __init__(self):
        try:
            pygame.mixer.init(frequency=RATE)
            self.disponible = True
        except Exception:
            self.disponible = False
        _generar_todos()
        self.sonidos = {}
        if self.disponible:
            for archivo in os.listdir(DIR):
                if archivo.endswith(".wav"):
                    nombre = archivo.replace(".wav", "")
                    ruta = os.path.join(DIR, archivo)
                    try:
                        self.sonidos[nombre] = pygame.mixer.Sound(ruta)
                    except Exception:
                        pass

    def reproducir(self, nombre):
        if self.disponible and nombre in self.sonidos:
            self.sonidos[nombre].play()
