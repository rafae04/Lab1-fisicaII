# electric_field.py
import numpy as np

def compute_field(charges, X, Y):
    Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
    for charge in charges:
        dEx, dEy = charge.field_at(X, Y)
        Ex += dEx
        Ey += dEy
    return Ex, Ey
