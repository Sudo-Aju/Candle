import pygame
import random
import math
from utils import global_noise

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 1.0
        self.time_alive = 0.0

    def update(self, wind: float):
        self.time_alive += 0.1

    def draw(self, surface):
        pass

class FireParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vel_x = random.uniform(-0.5, 0.5)
        self.vel_y = random.uniform(-4, -2)
        self.color = [255, 220, 50]

    def update(self, wind: float):
        super().update(wind)
        noise_offset = global_noise.get_noise(self.time_alive + self.y) * 2
        self.x += self.vel_x + (wind * 15) + noise_offset
        self.y += self.vel_y
        self.life -= 0.03 + (wind * 0.05)
        self.color[1] = max(0, self.color[1] - 5)
        if self.life < 0.4:
            self.color[0] = max(100, self.color[0] - 5)

    def draw(self, surface):
        radius = int(self.life * 12)
        if radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)

class SmokeParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vel_y = random.uniform(-2.0, -0.5)
        self.vel_x = random.uniform(-0.5, 0.5)
        self.life_decay = random.uniform(0.005, 0.01)
        self.radius = random.uniform(5, 10)
        self.max_radius = random.uniform(30, 50)
        shade = random.randint(100, 180)
        self.color = (shade, shade, shade)

    def update(self, wind: float):
        super().update(wind)
        self.x += (math.sin(self.time_alive) * 1.5) + self.vel_x + (wind * 5)
        self.y += self.vel_y
        if self.radius < self.max_radius:
            self.radius += 0.3
        self.life -= self.life_decay

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life * 100)
            size = int(self.radius * 2)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (int(self.radius), int(self.radius)), int(self.radius))
            surface.blit(surf, (int(self.x - self.radius), int(self.y - self.radius)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit_fire(self, x, y, count=5, dx=0):
        for _ in range(count):
            self.particles.append(FireParticle(x + dx, y))
            
    def emit_smoke(self, x, y, count=1, dx=0):
        for _ in range(count):
            self.particles.append(SmokeParticle(x + dx, y))
            
    def update_and_draw(self, surface, wind: float):
        for p in self.particles[:]:
            p.update(wind)
            if p.life <= 0:
                self.particles.remove(p)
            else:
                p.draw(surface)
    
    def clear(self):
        self.particles.clear()