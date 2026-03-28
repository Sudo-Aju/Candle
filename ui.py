import pygame

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.display_intensity = 0.0 

    def draw_meter(self, surface, current_intensity, limit):
        self.display_intensity += (current_intensity - self.display_intensity) * 0.1
        
        bar_width = 300
        bar_height = 20
        x = (self.width - bar_width) // 2
        y = self.height - 50

        pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height), border_radius=10)
        fill_width = min(bar_width, int((self.display_intensity / limit) * bar_width))
        color = (0, 255, 0) if self.display_intensity < limit * 0.8 else (255, 0, 0)
        
        if fill_width > 0:
            pygame.draw.rect(surface, color, (x, y, fill_width, bar_height), border_radius=10)
        
        text = self.font.render(f"Wind Power", True, (255, 255, 255))
        surface.blit(text, (x + 95, y - 30))

    def draw_text_center(self, surface, text, y_offset=0, size="normal"):
        font_to_use = self.title_font if size == "large" else self.font
        img = font_to_use.render(text, True, (255, 255, 255))
        rect = img.get_rect(center=(self.width // 2, (self.height // 2) + y_offset))
        surface.blit(img, rect)