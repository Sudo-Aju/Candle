import math
import random
from typing import List

class NoiseGenerator:
    """Custom 1D Perlin-style noise for organic fire movement."""
    def __init__(self, seed: int = None):
        if seed is None:
            seed = random.randint(0, 255)
        self.permutation: List[int] = list(range(256))
        random.Random(seed).shuffle(self.permutation)
        self.permutation += self.permutation 

    def _fade(self, t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t: float, a: float, b: float) -> float:
        return a + t * (b - a)

    def _grad(self, hash_value: int, x: float) -> float:
        h = hash_value & 15
        grad = 1.0 + (h & 7)
        if h & 8:
            grad = -grad
        return grad * x

    def get_noise(self, x: float) -> float:
        X = int(math.floor(x)) & 255
        x = x - math.floor(x)
        u = self._fade(x)
        A = self.permutation[X]
        B = self.permutation[X + 1]
        res = self._lerp(u, self._grad(A, x), self._grad(B, x - 1))
        return max(-1.0, min(1.0, res * 0.395))

global_noise = NoiseGenerator() 