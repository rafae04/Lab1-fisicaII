import numpy as np
import matplotlib.pyplot as plt
from jinja2 import Template
import pdfkit
import os

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
# Campo Eléctrico en un punto 
# ======================

x_test, y_test = 2.0, 2.0
Ex_total, Ey_total = compute_field(charges,x_test, y_test)  # tu función
E_modulo = np.sqrt(Ex_total**2 + Ey_total**2)
angulo = np.degrees(np.arctan2(Ey_total, Ex_total))

campo_resultado = {
    "x": x_test,
    "y": y_test,
    "Ex": round(float(Ex_total), 3),
    "Ey": round(float(Ey_total), 3),
    "modulo": round(float(E_modulo), 3),
    "angulo": round(float(angulo), 2)
}

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
threshold = 1e8
E_filtered[np.abs(E_filtered) > threshold] = np.nan

# ======================
# Encontrar puntos de equilibrio en E(x) (cruce por cero)
# ======================
zero_crossings = np.where(np.diff(np.sign(E_total)))[0]

# Posiciones de las cargas
charge_positions = [charge.x for charge in charges]
tol = 1e-2  # Tolerancia de cercanía a una carga

equilibrium_points = []         # Todos los cruces por cero
real_equilibrium_points = []   # Solo los que no están en posiciones de carga

for idx in zero_crossings:
    x0, x1 = xs[idx], xs[idx + 1]
    y0, y1 = E_total[idx], E_total[idx + 1]
    # Interpolación lineal
    x_eq = x0 - y0 * (x1 - x0) / (y1 - y0)
    equilibrium_points.append(x_eq)

    # Excluir si está muy cerca de una carga
    if not any(np.isclose(x_eq, xc, atol=tol) for xc in charge_positions):
        real_equilibrium_points.append(x_eq)


# ======================
# Graficar E(x) con puntos de equilibrio y cargas
# ======================
plt.figure()
plt.plot(xs, E_filtered, label='E(x) total', color='red')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)

# Puntos de equilibrio reales
plt.scatter(real_equilibrium_points, [0] * len(real_equilibrium_points),
            color='green', s=50, label='Puntos de equilibrio')

# Posiciones de las cargas
for xc in charge_positions:
    plt.axvline(x=xc, color='purple', linestyle=':', linewidth=1, label='Carga' if xc == charge_positions[0] else "")

plt.title('Campo Eléctrico E(x) sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('E(x) (N/C)')
plt.grid(True)
plt.legend()
plt.savefig("Ex_vs_x_con_equilibrio.png")
plt.show()

# ======================
# Graficar E(x) individuales por carga 
# ======================
colors = ['green', 'blue', 'orange']
exclusion_radius = 0.01  # 1 cm de exclusión alrededor de la carga

for i, charge in enumerate(charges):
    xs_q, E_q = compute_1d_field_or_potential([charge], axis='x', fixed_coord=0, points=2000, mode='field')
    
    # Filtrar valores cercanos a la carga (asíntota)
    E_q_filtered = np.copy(E_q)
    E_q_filtered[np.abs(xs_q - charge.x) < exclusion_radius] = np.nan
    
    plt.figure()
    plt.plot(xs_q, E_q_filtered, label=f'E(x) q{i+1} = {charge.q*1e6:.0f} μC', color=colors[i], linestyle='--')
    plt.axhline(0, color='black', linestyle=':', linewidth=0.8)
    plt.title(f'Campo Eléctrico E(x) de q{i+1} sobre el eje x')
    plt.xlabel('x (m)')
    plt.ylabel('E(x) (N/C)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Exq{i+1}_vs_x.png")
    plt.close()


# ======================
# Potencial V(x) sobre el eje x
# ======================
xs, V_total = compute_1d_field_or_potential(charges, axis='x', fixed_coord=0, mode='potential')

plt.figure()
plt.plot(xs, V_total, label='V(x) total', color='blue')

# Posiciones de las cargas
for i, xc in enumerate(charge_positions):
    plt.axvline(x=xc, color='purple', linestyle=':', linewidth=1, label='Carga' if i == 0 else "")

plt.title('Potencial Eléctrico V(x) sobre el eje x')
plt.xlabel('x (m)')
plt.ylabel('V(x) (V)')
plt.grid(True)
plt.legend()
plt.savefig("Vx_vs_x.png")
plt.show()



#-------------------
#Generación del PDF
#-------------------

# Formatear puntos para el HTML
puntos_formateados = [f"x = {p:.5f} m" for p in real_equilibrium_points]

# Leer index.html
folder = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(folder, "index.html")

with open(html_path, "r", encoding="utf-8") as f:
    html_base = f.read()

# Renderizar HTML con Jinja2
template = Template(html_base)
rendered_html = template.render(puntos=puntos_formateados,
    campo=campo_resultado)

# Guardar HTML renderizado temporalmente
rendered_html_path = os.path.join(folder, "index_rendered.html")
with open(rendered_html_path, "w", encoding="utf-8") as f:
    f.write(rendered_html)

# Configurar wkhtmltopdf  (debe descargar y agregar a PATH previamente https://wkhtmltopdf.org/downloads.html )
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
options = {'enable-local-file-access': None}

# Generar PDF
pdf_output_path = os.path.join(folder, "informe_final.pdf")
pdfkit.from_file(rendered_html_path, pdf_output_path, options=options, configuration=config)

print(f"PDF generado correctamente en: {pdf_output_path}")
