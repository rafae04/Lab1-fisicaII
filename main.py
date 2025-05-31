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

# Recalcular con más puntos para mayor precisión
xs, E_total = compute_1d_field_or_potential(charges, axis='x', fixed_coord=0, points=2000, mode='field')

# Eliminar valores extremos (que representan asintotas reales, cerca de las cargas)
E_filtered = np.copy(E_total)
threshold = 1e8  # valor límite para cortar (ajustalo según escala de tus cargas)
E_filtered[np.abs(E_filtered) > threshold] = np.nan  # reemplaza con NaN para no graficarlos

#graficar
plt.figure()
plt.plot(xs, E_filtered, label='E(x) total', color='red')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.title('Campo Eléctrico E(x) sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()

plt.savefig("Ex_vs_x.png")
plt.show()

# ======================
# E(x) q1 sobre el eje x
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

# ======================
# E(x) q2 sobre el eje x
# ======================
xs_q2, E_q2 = compute_1d_field_or_potential([charges[1]], axis='x', fixed_coord=0, points=2000, mode='field')
plt.plot(xs_q2, E_q2, label=f'E(x) q2 = {charges[1].q*1e6:.0f} μC', color='blue', linestyle='--')
plt.figure()
plt.title('Campo Eléctrico E(x) de q2 sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()
plt.savefig("Exq2_vs_x.png")

# ======================
# E(x) q3 sobre el eje x
# ======================
xs_q3, E_q3 = compute_1d_field_or_potential([charges[2]], axis='x', fixed_coord=0, points=2000, mode='field')
plt.plot(xs_q3, E_q3, label=f'E(x) q3 = {charges[2].q*1e6:.0f} μC', color='orange', linestyle='--')
plt.figure()
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

# Supón que ya tienes Ex, Ey, X, Y calculados
E_magnitude = np.sqrt(Ex*2 + Ey*2)
threshold = 1e-3  # Ajusta este valor según la escala de tu campo

# Encuentra los índices donde el campo es casi cero
zeros = np.where(E_magnitude < threshold)

# Extrae las coordenadas de esos puntos
x_eq = X[zeros]
y_eq = Y[zeros]

# Puedes imprimirlos o graficarlos
print("Puntos de equilibrio:")
for x, y in zip(x_eq, y_eq):
    print(f"x = {x:.3f}, y = {y:.3f}")

# Para graficar sobre tu campo:
plt.plot(x_eq, y_eq, 'go', markersize=8, label='Campo ≈ 0')
plt.legend()

# Busca los índices donde E(x) cambia de signo (cruza por cero)
cero_indices = np.where(np.diff(np.sign(E_total)))[0]

# Umbral para considerar "cerca" de una carga (ajustá según resolución de xs)
umbral = 1e-2

print("Punto(s) de equilibrio donde E(x) ≈ 0:")
for idx in cero_indices:
    x_cero = (xs[idx] + xs[idx+1]) / 2
    if np.all(np.abs(x_cero - x_cargas) > umbral):
        print(f"x ≈ {x_cero:.3f} m")