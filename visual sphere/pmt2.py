import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d

def plot_cylinder(ax, x, y, z, r, h, color='r'):
    # Cylinder base
    p = Circle((x, y), radius=r, color=color, ec='black')
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
    
    # Cylinder top
    p2 = Circle((x, y), radius=r, color=color, ec='black')
    ax.add_patch(p2)
    art3d.pathpatch_2d_to_3d(p2, z=z+h, zdir="z")
    # Cylinder surface
    theta = np.linspace(0, 2*np.pi, 50)
    z_grid = np.linspace(0, h, 50)
    theta_grid, Z = np.meshgrid(theta, z_grid)
    X = r * np.cos(theta_grid) + x
    Y = r * np.sin(theta_grid) + y
    ax.plot_surface(X, Y, Z + z, color=color)
    return X,Y,Z

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def main():
    X,Y,Z = plot_cylinder(ax, 1, 2, 0, 1, 3, color='blue')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-2, 4])
    ax.set_ylim([-1, 5])
    ax.set_zlim([0, 4])
    plt.show()
    # print(X,Y,Z)
    
    

if __name__ == "__main__":
    main()