import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#  Utility Functions 
from sphere_coord import generate_sphere, sphere_bound_testing
from crystal import make_box
from pmt import make_pmt, rotate_x_90


'''Sphere Variables'''
R = 1  # Radius of the sphere (cm)
n = 1000  # Number of random points
point_size = 1 # in points cubed, convert to cm by dividing by 22780
epsilon = np.finfo(float).eps

''' Distance variables'''
d1 = 3  #crystal to points (for later optimizing)
d2 = 0 #detector to sphere
buffer = .5

'''Model Variables'''
xmin, ymin, zmin = (-R - d2 - buffer ) , 0, 0
xmax, ymax, zmax = (R + d1 + buffer), 5, 27 #need to optimize x
alpha_c = .3 #transparency values
alpha_s = .8
alpha_p = .8

''' Crystal Variables'''
length, width, height= cl, cw, ch = 2.05, 2.05, 20 # crystal dimensions (cm)
xo_c, yo_c, zo_c = x_pos, y_pos, z_pos = d1, 0, 0 # crystal origin coords


'''PMT Vaviables'''
pmt_length = .859 # Measured (cm)
rp = .3925  



def display(crystal, X_full, Y_full, Z_full, xp, yp, zp):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  
    
    #Plot points
    ax.add_collection3d(crystal)
    ax.scatter(X_full, Y_full, Z_full, color="royalblue", s=point_size, alpha= alpha_s)
    ax.plot_surface(xp, yp, zp, alpha = alpha_p, color = "r") #, edgecolor = 'k'
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)

    # Automatically calculate aspect ratio
    ax.set_box_aspect([
        xmax - xmin,
        ymax - ymin,
        zmax - zmin
    ])
    # plt.show()


def main():
    xs, ys, zs = generate_sphere()
    sphere_bound_testing(xs, ys, zs)
    xp, yp, zp = make_pmt(rp,pmt_length)
    xc_pos, yc_pos, zc_pos = (xmax - buffer), ymax/2, 0 #crystal positioning
    
    xs += 0 #sphere is aligned a 0
    ys += yc_pos + cw/2 # Align sphere with center of crystal
    zs += zc_pos + ch/2  # Mid-height of the box
    
    crystal = make_box()
    display(crystal, xs, ys, zs, xp, yp, zp)
    plt.show()

if __name__ == "__main__":
    main()
