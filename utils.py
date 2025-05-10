# utils.py
import numpy as np

def compute_1d_field_or_potential(charges, axis='x', fixed_coord=0, points=200, mode='field'):
    xs = np.linspace(-5, 5, points)
    ys = np.full_like(xs, fixed_coord)
    values = []

    for x, y in zip(xs, ys):
        if mode == 'field':
            total_Ex = sum(c.field_at(x, y)[0] for c in charges)
            values.append(total_Ex)
        elif mode == 'potential':
            total_V = sum(c.potential_at(x, y) for c in charges)
            values.append(total_V)

    return xs, np.array(values)
