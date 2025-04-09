import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#  Utility Functions 
from sphere_coord import generate_sphere, show_sphere, sphere_bound_testing
from crystal import make_box, show_box

# Parameters
R = 1  # Radius of the sphere
n = 10000  # Number of random points
epsilon = np.finfo(float).eps
length, width, height = 2.05, 2.05, 20 # crystal dimensions

d1 = 3  #crystal to points (for later optimizing)
d2 = 0 #detector to sphere
buffer = .5
xmin, ymin, zmin = 0,0,0
xmax, ymax, zmax = (2*R + d1 +d2 + buffer), 5, 27


def display(crystal,X_full, Y_full, Z_full):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  
    
    #Plot points
    ax.add_collection3d(crystal)
    ax.scatter(X_full, Y_full, Z_full, color="royalblue", s=3, alpha=0.8)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)

    # Automatically calculate aspect ratio
    ax.set_box_aspect([
        xmax - xmin,
        ymax - ymin,
        zmax - zmin
    ])
    plt.show()


def main():
    X_full,Y_full,Z_full = generate_sphere()
    sphere_bound_testing(X_full,Y_full,Z_full)

    x_pos, y_pos, z_pos = xmax - buffer, ymax/2, 0 #crystal positioning
    
    X_full += .5 + d2 + R # Align sphere with center of crystal
    Y_full += y_pos + width/2 
    Z_full += z_pos + height/2  # Mid-height of the box

    
    crystal = make_box()
    display(crystal,X_full, Y_full, Z_full)

if __name__ == "__main__":
    main()
