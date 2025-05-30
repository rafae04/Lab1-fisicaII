import matplotlib.pyplot as plt
import numpy as np

def plot_field_lines(X, Y, Ex, Ey, charges=None, filename=None):
    plt.figure()
    plt.streamplot(X, Y, Ex, Ey, color=np.sqrt(Ex**2 + Ey**2), cmap='inferno')
    plt.title('Líneas de Campo Eléctrico')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True)

    # Agregar cargas
    if charges:
        for charge in charges:
            color = 'red' if charge.q > 0 else 'blue'
            plt.plot(charge.x, charge.y, 'o', color=color, markersize=10)

    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def plot_potential_contours(X, Y, V, charges=None, filename=None):
    plt.figure()
 # Definir niveles manualmente desde el mínimo al máximo
    niveles = np.linspace(np.min(V), np.max(V), 1000) 
    cp = plt.contour(X, Y, V, levels=niveles, colors='black', linewidths=0.5)

    plt.title('Líneas Equipotenciales')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.xlim(-2, 2)
    plt.ylim(-1.5, 1.5)
    plt.grid(True)

    # Agregar cargas
    if charges:
        for charge in charges:
            color = 'red' if charge.q > 0 else 'blue'
            plt.plot(charge.x, charge.y, 'o', color=color, markersize=10)

    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()
