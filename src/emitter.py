import random
import math
from .particle import Particle
from .config import FIRE_COLORS

class Emitter:
    def __init__(self, x, y, emit_rate=10):
        self.x = x
        self.y = y
        self.emit_rate = emit_rate
        self.particles = []
        self.emit_accum = 0  # accumulated time for emission
    def emit(self):
        # simple particle emission logic, random vector and speed and life
        angle = random.uniform(0, 2 * 3.14159)  # Random angle in radians
        speed = random.uniform(0.5, 2.0)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        life = random.uniform(1.0, 3.0)
        particle = Particle(
            self.x, 
            self.y, 
            vx, 
            vy, 
            life, 
            size=random.uniform(0.5, 2.0),  # Random size
            color = FIRE_COLORS[random.randint(0, len(FIRE_COLORS) - 1)]  # Random color from FIRE_COLORS
        )
        self.particles.append(particle)
    def update(self, dt):
        self.emit_accum += dt *self.emit_rate
        while self.emit_accum >= 1.0:
            self.emit()
            self.emit_accum -= 1.0
        for particle in self.particles:
            particle.update(dt)
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]