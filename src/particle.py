class Particle:
    #def __init__(self, x, y, vx, vy, life, size=1.0, color=(1, 1, 1, 1)):
    #    self.x = x
    #    self.y = y
    #    self.vx = vx
    #    self.vy = vy
    #    self.life = life
    #    self.max_life = life
    #    self.size = size
    #    self.color = color
    #    self.gravity = -50  # Gravity effect on the particle
    def __init__(self, x, y, vx, vy, life, size=1.0, color=(1, 1, 1, 1)):
        self.reset(x, y, vx, vy, life, size, color)        
    def update(self, dt):
        self.vy += self.gravity * dt
        self.x += self.vx * dt *0.98
        self.y += self.vy * dt *0.90
        self.life -= dt
        if self.life < 0:
            self.life = 0
        else:
            alpha = self.life / self.max_life
            self.color = (self.color[0], self.color[1], self.color[2], alpha)
    def is_alive(self):
        return self.life > 0    
    
    def reset(self, x, y, vx, vy, life, size=1.0, color=(1, 1, 1, 1)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.size = size
        self.color = color
        self.gravity = -50
        self.is_ember = False
    
    