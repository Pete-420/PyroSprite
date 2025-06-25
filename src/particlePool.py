from .particle import Particle

class ParticlePool:
    def __init__(self, max_particles=1000):
        self.max_particles = max_particles
        self.active_particles = []
        self.inactive_particles = []
        
        # Pre-allocate all particles
        for _ in range(max_particles):
            particle = Particle(0, 0, 0, 0, 0)
            self.inactive_particles.append(particle)
    
    def get_particle(self):
        if self.inactive_particles:
            particle = self.inactive_particles.pop()
            self.active_particles.append(particle)
            return particle
        return None
    
    def return_particle(self, particle):
        if particle in self.active_particles:
            self.active_particles.remove(particle)
            self.inactive_particles.append(particle)
    
    def update_all(self, dt):
        dead_particles = []
        
        for particle in self.active_particles:
            particle.update(dt)
            if not particle.is_alive():
                dead_particles.append(particle)
        
        # Return dead particles to pool
        for particle in dead_particles:
            self.return_particle(particle)
    
    def get_active_count(self):
        return len(self.active_particles)
    
    def get_available_count(self):
        return len(self.inactive_particles)