import numpy as np
import config

class Charge:
    def __init__(self, q, x, y):
        self.q = q
        self.x = x
        self.y = y

    def field_at(self, x, y):
        dx = x - self.x
        dy = y - self.y
        r_squared = dx**2 + dy**2
        r = np.sqrt(r_squared)
        r_cubed = r_squared * r + 1e-20  # evitar división por cero
        Ex = config.K * self.q * dx / r_cubed
        Ey = config.K * self.q * dy / r_cubed
        return Ex, Ey

    def potential_at(self, x, y):
        dx = x - self.x
        dy = y - self.y
        r = np.sqrt(dx**2 + dy**2) + 1e-20
        return config.K * self.q / r
