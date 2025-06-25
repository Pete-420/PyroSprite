import random
import math
import time
from .particle import Particle
from .config import FIRE_COLORS
from .particlePool import ParticlePool

class Emitter:
    def __init__(self, x, y, emit_rate=10, max_particles=1000):
        self.x = x
        self.y = y
        self.emit_rate = emit_rate
        #self.particles = []
        self.emit_accum = 0  
        self.particle_pool = ParticlePool(max_particles)
    def emit(self):
        base_width = 30 
        
        particle = self.particle_pool.get_particle()
        if not particle:
            return #basen jest pełny, nie emitować więcej cząstek
        emit_x = self.x + random.uniform(-base_width/2, base_width/2)
        emit_y = self.y
        
        is_small_pice_of_fire = random.random() < 0.1  # 10% szans na iskrę
        
        # Im dalej od środka, tym bardziej skośny płomień
        distance_from_center = abs(emit_x - self.x) / (base_width/2)
        angle_bias = distance_from_center * math.pi / 8  
        if emit_x < self.x:
            angle_bias = -angle_bias
            
        flicker_fast = math.sin(time.time() * 8) * 0.3
        flicker_slow = math.sin(time.time() * 3) * 0.2
        flicker_random = math.sin(time.time() * 12 + self.x * 0.1) * 0.1
        
        total_flicker = flicker_fast + flicker_slow + flicker_random
        speed_modifier = 1.0 + total_flicker * 0.5
        angle_modifier = total_flicker * 0.3
        size_modifier = 1.0 + total_flicker * 0.4
        if is_small_pice_of_fire: #iskierka
            speed = random.uniform(2.0, 4.0) * speed_modifier
            angle = random.uniform(-math.pi/3, math.pi/3) + angle_bias 
            angle += math.pi / 2  # base_angle
            life_base = random.uniform(0.5, 1.5)
            size_base = random.uniform(0.2, 0.8)
            color = (1.0, 0.4, 0.1, 1.0)
        else:
            angle = random.uniform(-math.pi/4, math.pi/4) + angle_bias + angle_modifier
            angle += math.pi / 2  # base_angle
            speed = random.uniform(0.5, 2.0) * speed_modifier
            life_base = random.uniform(1.0, 3.0)
            size_base = random.uniform(0.5, 2.0)
            color = FIRE_COLORS[random.randint(0, len(FIRE_COLORS) - 1)]
        
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        life = life_base * (1.0 - distance_from_center * 0.3)
        size = size_base * size_modifier * (1.0 + distance_from_center * 0.2)
        #particle = Particle(emit_x, emit_y, vx, vy, life, size=size, color=color)
        particle.reset(emit_x,emit_y, vx, vy, life, size, color)
        # Ustaw dodatkowe właściwości dla iskierki
        particle.is_ember = is_small_pice_of_fire
        #self.particles.append(particle)
    def update(self, dt):
        self.emit_accum += dt *self.emit_rate
        while self.emit_accum >= 1.0:
            self.emit()
            self.emit_accum -= 1.0
#        for particle in self.particles:
#            particle.update(dt)
        self.particle_pool.update_all(dt)

    @property
    def particles(self):
        return self.particle_pool.active_particles
    def get_particle_stats(self):
        return {
            'active': self.particle_pool.get_active_count(),
            'available': self.particle_pool.get_available_count(),
            'total': self.particle_pool.max_particles
        }