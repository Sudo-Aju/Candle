import pygame
import random

class FireParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-0.5, 0.5)
        self.vel_y = random.uniform(-4, -2)
        self.life = 1.0
        self.color = [255, 220, 50]

    def update(self, wind: float):
        self.x += self.vel_x + (wind * 15)
        self.y += self.vel_y
        self.life -= 0.03 + (wind * 0.05)
        
        self.color[1] = max(0, self.color[1] - 5)
        if self.life < 0.4:
            self.color[0] = max(100, self.color[0] - 5)

    def draw(self, surface):
        radius = int(self.life * 12)
        if radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit_fire(self, x, y, count=5):
        for _ in range(count):
            self.particles.append(FireParticle(x, y))
            
    def update_and_draw(self, surface, wind: float):
        for p in self.particles[:]:
            p.update(wind)
            if p.life <= 0:
                self.particles.remove(p)
            else:
                p.draw(surface)
    
    def clear(self):
        self.particles.clear()