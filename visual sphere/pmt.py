import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


r = 1 # Need to measure, but let's say the rad = 10mm
pmt_lenth = np.linspace(0, 10, 100)
alpha_p = .8

fig = plt.figure(facecolor= "Black")
ax = plt.axes(projection = "3d")
plt.axis("off")
ax.set_facecolor("Cyan")

def make_pmt(r, length):
    theta = np.linspace(0, 2*np.pi, 100)
    z = length
    theta_grid, z_grid = np.meshgrid(theta, z)

    X = r * np.cos(theta_grid)
    Y = r * np.sin(theta_grid)
    Z = z_grid

    X, Y, Z = rotate_x_90(X,Y,Z)
    return X, Y, Z


def rotate_x_90(x, y, z):
    # Apply the 90 degree rotation matrix around the x-axis
    x_rot = x
    y_rot = -z  # y = -z for a 90-degree rotation around x-axis
    z_rot = y
    return x_rot, y_rot, z_rot

def show_pmt(X, Y, Z):
    ax.plot_surface(X, Y, Z, alpha = alpha_p, edgecolor = 'k')
    # ax.plot_surface(X, Y, Z, rstride = 10, cstride = 10, cmap = cm.RdPu)
    return fig,
   

def main():
    X,Y,Z = make_pmt(r, pmt_lenth)
    ax.plot_surface(X, Y, Z, alpha = alpha_p, edgecolor = 'k')
    plt.show()
    # print(X, Y, Z)

if __name__ == "__main__":
    main()


