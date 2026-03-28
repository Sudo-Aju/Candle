import pygame
import os
from typing import Dict, Tuple, Optional

class AssetManager:
    """Caches and scales images to prevent memory leaks."""
    def __init__(self, base_path: str = "assets"):
        self.base_path = base_path
        self.cache: Dict[str, pygame.Surface] = {}
        
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _create_fallback_surface(self, width: int, height: int, color: Tuple[int, int, int]) -> pygame.Surface:
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill(color)
        pygame.draw.rect(surf, (255, 0, 0), surf.get_rect(), 2) 
        return surf

    def load_image(self, filename: str, scale_to: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        cache_key = f"{filename}_{scale_to}" if scale_to else filename
        if cache_key in self.cache:
            return self.cache[cache_key]

        filepath = os.path.join(self.base_path, filename)
        try:
            image = pygame.image.load(filepath).convert_alpha()
            if scale_to:
                image = pygame.transform.smoothscale(image, scale_to)
            self.cache[cache_key] = image
            return image
        except FileNotFoundError:
            fallback = self._create_fallback_surface(
                scale_to[0] if scale_to else 100, 
                scale_to[1] if scale_to else 100, 
                (255, 0, 255, 128)
            )
            self.cache[cache_key] = fallback
            return fallback