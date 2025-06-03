# main.py
import numpy as np
import matplotlib.pyplot as plt

import config
from charges import Charge
from electric_field import compute_field
from potential import compute_potential
from plotting import plot_field_lines, plot_potential_contours
from utils import compute_1d_field_or_potential

# Crear las cargas
charges = [
    Charge(+20e-6, -1.5, 0),
    Charge(30e-6, 0, 0),
    Charge(-40e-6, 0.5, 0)
]

# Crear malla 2D
x = np.linspace(*config.X_RANGE, config.GRID_SIZE)
y = np.linspace(*config.Y_RANGE, config.GRID_SIZE)
X, Y = np.meshgrid(x, y)

# ======================
# Campo Eléctrico
# ======================
Ex, Ey = compute_field(charges, X, Y)
plot_field_lines(X, Y, Ex, Ey, charges=charges, filename="campo_electrico.png")

# ======================
# Potencial Eléctrico
# ======================
V = compute_potential(charges, X, Y)
plot_potential_contours(X, Y, V, charges=charges, filename="potencial_electrico.png")

# ======================
# E(x) sobre el eje x
# ======================
xs, E_total = compute_1d_field_or_potential(charges, axis='x', fixed_coord=0, points=2000, mode='field')

# Eliminar valores extremos (asintotas)
E_filtered = np.copy(E_total)
threshold = 1e8  # Ajusta según escala de tus cargas
E_filtered[np.abs(E_filtered) > threshold] = np.nan

# ======================
# Encontrar puntos de equilibrio en E(x) (cruce por cero)
# ======================
zero_crossings = np.where(np.diff(np.sign(E_total)))[0]

equilibrium_points = []
for idx in zero_crossings:
    x0, x1 = xs[idx], xs[idx+1]
    y0, y1 = E_total[idx], E_total[idx+1]
    # Interpolación lineal para estimar raíz
    x_eq = x0 - y0 * (x1 - x0) / (y1 - y0)
    equilibrium_points.append(x_eq)

print("Puntos de equilibrio (aproximados) en el eje x:")
for p in equilibrium_points:
    print(f"x = {p:.5f} m")

# Graficar E(x) y puntos de equilibrio
plt.figure()
plt.plot(xs, E_filtered, label='E(x) total', color='red')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.scatter(equilibrium_points, [0]*len(equilibrium_points), color='green', s=50, label='Puntos equilibrio')
plt.title('Campo Eléctrico E(x) sobre el eje x con puntos de equilibrio')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()
plt.savefig("Ex_vs_x_con_equilibrio.png")
plt.show()

# ======================
# Graficar y guardar E(x) individuales por carga (como ya tenías)
# ======================
xs_q1, E_q1 = compute_1d_field_or_potential([charges[0]], axis='x', fixed_coord=0, points=2000, mode='field')
plt.figure()
plt.plot(xs_q1, E_q1, label=f'E(x) q1 = {charges[0].q*1e6:.0f} μC', color='green', linestyle='--')
plt.title('Campo Eléctrico E(x) de q1 sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()
plt.savefig("Exq1_vs_x.png")

xs_q2, E_q2 = compute_1d_field_or_potential([charges[1]], axis='x', fixed_coord=0, points=2000, mode='field')
plt.figure()
plt.plot(xs_q2, E_q2, label=f'E(x) q2 = {charges[1].q*1e6:.0f} μC', color='blue', linestyle='--')
plt.title('Campo Eléctrico E(x) de q2 sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()
plt.savefig("Exq2_vs_x.png")

xs_q3, E_q3 = compute_1d_field_or_potential([charges[2]], axis='x', fixed_coord=0, points=2000, mode='field')
plt.figure()
plt.plot(xs_q3, E_q3, label=f'E(x) q3 = {charges[2].q*1e6:.0f} μC', color='orange', linestyle='--')
plt.title('Campo Eléctrico E(x) de q3 sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()
plt.savefig("Exq3_vs_x.png")

# ======================
# V(x) sobre el eje x
# ======================
xs, V_total = compute_1d_field_or_potential(charges, axis='x', fixed_coord=0, mode='potential')
plt.figure()
plt.plot(xs, V_total, label='V(x) total', color='blue')
plt.title('Potencial Eléctrico V(x) sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('V(x) (V)')
plt.grid(True)
plt.legend()
plt.savefig("Vx_vs_x.png")