# potential.py
import numpy as np

def compute_potential(charges, X, Y):
    V = np.zeros_like(X)
    for charge in charges:
        V += charge.potential_at(X, Y)
    return V
