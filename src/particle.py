class Particle:
    def __init__(self, x, y, vx, vy, life, size=1.0, color=(1, 1, 1, 1)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.size = size
        self.color = color
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        if self.life < 0:
            self.life = 0
    def is_alive(self):
        return self.life > 0    
    
    