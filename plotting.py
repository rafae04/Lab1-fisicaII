import matplotlib.pyplot as plt
import numpy as np

def plot_field_lines(X, Y, Ex, Ey, charges=[], extra_points=None, filename=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Dibujar líneas de campo
    ax.streamplot(X, Y, Ex, Ey, color='black', linewidth=1, density=1.5, arrowsize=1)
    
    # Dibujar cargas
    for charge in charges:
        color = 'red' if charge.q > 0 else 'blue'
        ax.plot(charge.x, charge.y, 'o', color=color, markersize=10,
                markeredgecolor='black', markeredgewidth=1.5)

    # Dibujar puntos extra si se pasan
    if extra_points:
        xs, ys = zip(*extra_points)
        ax.plot(xs, ys, 'o', color='green', markersize=10,
                markeredgecolor='black', markeredgewidth=1.2)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.grid(True)
    
    if filename:
        plt.savefig(filename, dpi=300)
    else:
        plt.show()

    plt.close()


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

def plot_plano(X, Y, charges=None, filename=None):
    plt.figure()
    plt.title('Plano XY')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    plt.grid(True)


     # Agregar cargas
    if charges:
        for charge in charges:
            color = 'red' if charge.q > 0 else 'blue'
            plt.plot(charge.x, charge.y, 'o', color=color, markersize=10, markeredgecolor='black', markeredgewidth=1.5)

    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()
