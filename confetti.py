import pygame
import random
import math
from typing import List

class Confetti:
    def __init__(self, screen_width: int, screen_height: int):
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(-500, -50) 
        self.width = random.randint(8, 15)
        self.height = random.randint(10, 20)
        colors = [(255, 50, 50), (50, 255, 50), (50, 50, 255), 
                  (255, 255, 50), (255, 50, 255), (50, 255, 255)]
        self.color = random.choice(colors)
        self.speed_y = random.uniform(2.0, 5.0)
        self.speed_x = random.uniform(-1.0, 1.0)
        self.rotation_speed = random.uniform(0.05, 0.2)
        self.rotation = random.uniform(0, math.pi * 2)
        self.drift_offset = random.uniform(0, 100)

    def update(self) -> None:
        self.y += self.speed_y
        self.x += math.sin(self.y * 0.02 + self.drift_offset) + self.speed_x
        self.rotation += self.rotation_speed

    def draw(self, surface: pygame.Surface) -> None:
        current_width = max(1.0, abs(math.cos(self.rotation) * self.width))
        rect = pygame.Rect(
            int(self.x - current_width / 2), int(self.y - self.height / 2), 
            int(current_width), int(self.height)
        )
        pygame.draw.rect(surface, self.color, rect)

class CelebrationManager:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.confetti_list: List[Confetti] = []
        self.is_active = False

    def trigger(self, amount: int = 150) -> None:
        self.is_active = True
        self.confetti_list = [Confetti(self.width, self.height) for _ in range(amount)]

    def update_and_draw(self, surface: pygame.Surface) -> None:
        if not self.is_active:
            return
        active_confetti = []
        for c in self.confetti_list:
            c.update()
            c.draw(surface)
            if c.y < self.height + 50:
                active_confetti.append(c)
        self.confetti_list = active_confetti
        if len(self.confetti_list) == 0:
            self.is_active = False

    def reset(self) -> None:
        """Clears all confetti and resets the celebration state."""
        self.confetti_list.clear()
        self.is_active = False