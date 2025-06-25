import random
import math
import time
from .particle import Particle
from .config import FIRE_COLORS

class Emitter:
    def __init__(self, x, y, emit_rate=10):
        self.x = x
        self.y = y
        self.emit_rate = emit_rate
        self.particles = []
        self.emit_accum = 0  
    def emit(self):
        base_width = 30 
        emit_x = self.x + random.uniform(-base_width/2, base_width/2)
        emit_y = self.y
              # Im dalej od środka, tym bardziej skośny płomień
        distance_from_center = abs(emit_x - self.x) / (base_width/2)
        
      
        angle_bias = distance_from_center * math.pi / 8  # Większy kąt na brzegach
        if emit_x < self.x:
            angle_bias = -angle_bias
        flicker_fast = math.sin(time.time() * 8) * 0.3    # Szybkie migotanie
        flicker_slow = math.sin(time.time() * 3) * 0.2    # Wolne pulsowanie
        flicker_random = math.sin(time.time() * 12 + self.x * 0.1) * 0.1  # Losowe zakłócenia (bo ładnie wygląda)
        
        total_flicker = flicker_fast + flicker_slow + flicker_random
        speed_modifier = 1.0 + total_flicker * 0.5
        angle_modifier = total_flicker * 0.3
        size_modifier = 1.0 + total_flicker * 0.4
        angle = random.uniform(-math.pi/4, math.pi/4) + angle_bias + angle_modifier
        base_angle = math.pi / 2
        angle += base_angle
        speed = random.uniform(0.5, 2.0) * speed_modifier
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        
        # Życie - dalsze od środka żyją krócej
        life_base = random.uniform(1.0, 3.0)
        life = life_base * (1.0 - distance_from_center * 0.3)  # Brzegi żyją 30% krócej
        
        # Rozmiar z flickering i pozycją
        size_base = random.uniform(0.5, 2.0)
        size = size_base * size_modifier * (1.0 + distance_from_center * 0.2)  # Brzegi nieco większe
        
        particle = Particle(
            emit_x,  # Używamy pozycji z szerokiej podstawy
            emit_y, 
            vx, 
            vy, 
            life, 
            size=size,
            color = FIRE_COLORS[random.randint(0, len(FIRE_COLORS) - 1)]
        )
        self.particles.append(particle)
    def update(self, dt):
        self.emit_accum += dt *self.emit_rate
        #turbulence_x = math.sin(time.time() * 2 + self.x * 0.1) * 0.5
        #turbulence_y = math.cos(time.time() * 1.5 + self.y * 0.1) * 0.3
        #self.vx += turbulence_x * dt
        #self.vy += turbulence_y * dt
        while self.emit_accum >= 1.0:
            self.emit()
            self.emit_accum -= 1.0
        for particle in self.particles:
            particle.update(dt)
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]