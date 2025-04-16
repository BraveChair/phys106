import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
from itertools import count
from multiprocessing import Process

'''Sphere Variables'''
R = 1  # Radius of the sphere (cm)
n = 10000  # Number of random points
point_size = 1 # in points cubed, convert to cm by dividing by 22780
epsilon = np.finfo(float).eps

'''PMT Vaviables'''
pmt_length = .859 # Measured (cm)
rp = .3925 # radius (cm)


''' Distance variables'''
d1 = .9  #crystal to points (for later optimizing)
d2 = 1.1 #detector to sphere
buffer = .5

''' Crystal Variables'''
length, width, height= 2.05, 2.05, 20 # crystal dimensions (cm)
xo_c, yo_c, zo_c = d1, 0, 0 # crystal origin coords

'''Model Variables'''
alpha_c = .8 #transparency values
alpha_s = .6
alpha_p = .8


def spheric2cartesian(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

def generate_sphere():
    # Generate random angles (Full sphere)
    theta = np.arccos(1 - 2 * np.random.rand(n))  # Theta: 0 to π
    phi =  2* np.pi * np.random.rand(n) #n  # Phi: 0 to 2π  
    return spheric2cartesian(R, theta, phi)

def sphere_bound_testing(X_full, Y_full, Z_full):
    coords = np.vstack([X_full, Y_full, Z_full])
    bad_points = np.any((coords < -R - epsilon) | (coords > R + epsilon), axis = 0)
    if np.any(bad_points):
        print("Bad Coordinates: ", coords[:,bad_points[1]])
        raise ValueError("DATA ERROR: Some points are outside the sphere bounds.")
    else: print("All points within bounds!")

def make_box(x_pos, y_pos, z_pos):
    vertices = np.array([
        [x_pos, y_pos, z_pos],
        [x_pos + length, y_pos, z_pos],
        [x_pos + length, y_pos + width, z_pos],
        [x_pos, y_pos + width, z_pos],
        [x_pos, y_pos, z_pos + height],
        [x_pos + length, y_pos, z_pos + height],
        [x_pos + length, y_pos + width, z_pos + height],
        [x_pos, y_pos + width, z_pos + height]
    ])
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7]
    ]
    triangles = []
    for face in faces:
        triangles.append([face[0], face[1], face[2]])
        triangles.append([face[0], face[2], face[3]])
    poly3d = Poly3DCollection([vertices[tri] for tri in triangles], color='black', alpha=alpha_c)
    return poly3d

def plot_cylinder(ax, x, y, z, r, h, color='green'):
    # Cylinder base
    bottom = Circle((y, z), radius=r, color=color)
    ax.add_patch(bottom)
    art3d.pathpatch_2d_to_3d(bottom, z=x, zdir="x")

    #Cylinder top
    top = Circle((y, z), radius=r, color=color)
    ax.add_patch(top)
    art3d.pathpatch_2d_to_3d(top, z=x-h, zdir="x")
    theta = np.linspace(0, 2*np.pi, 30)
    
    # Cylinder surface
    z_vals = np.linspace(0, h, 2)
    theta, Z = np.meshgrid(theta, z_vals)
    X = r * np.cos(theta)
    Y = r * np.sin(theta)
    X,Y,Z = rotate_xy_90(X,Y,Z)
    X += x
    Y += y
    Z += z
    return X,Y,Z

def rotate_xy_90(x, y, z):
    # Apply the 90 degree rotation matrix around the x-axis
    x_rot = -z
    y_rot = x  # y = -z for a 90-degree rotation around x-axis, y=x for rotating about z
    z_rot = y
    return x_rot, y_rot, z_rot

def find_limits(blah, axis):
    if blah.any():
        vari_min = np.min(blah[:, axis]) - buffer
        vari_max = np.max(blah[:, axis]) + buffer
        return vari_min, vari_max
    else: 
        raise IndexError("ERROR: Unbounded Graph limits")
    
def model(xs, ys, zs,vari_all, xop, yop, zop):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xs, ys, zs, color="blue", alpha=alpha_s, s=point_size) #add sphere
    ax.add_collection3d(make_box(xo_c, yo_c, zo_c)) #add crystal
    xp, yp, zp = plot_cylinder(ax, xop, yop, zop, rp, pmt_length) #add pmt
    ax.plot_surface(xp, yp, zp, color="green", alpha=alpha_p) 
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Autoscaler
    xmin, xmax = find_limits(vari_all, axis=0)
    ymin, ymax = find_limits(vari_all, axis=1)
    zmin, zmax = find_limits(vari_all, axis=2)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)
    ax.set_box_aspect([xmax - xmin, ymax - ymin, zmax - zmin])

    plt.tight_layout()
    plt.show()

def count_in_box(xs, ys, zs, lx, ly, lz):
    xo_c, yo_c, zo_c = d1, 0, 0

    inside_x = (xs >= xo_c) & (xs <= xo_c + lx) 
    inside_y = (ys >= yo_c) & (ys <= yo_c + ly)
    inside_z = (zs >= zo_c) & (zs <= zo_c + lz)

    inside = inside_x & inside_y & inside_z
    count = np.sum(inside)
    return count, inside
   
def opt_1(r, xs,ys,zs):
    count, mask = count_in_box(xs, ys, zs, lx = length, ly =width, lz=height)
    start_time = time.time()
    c_hits = np.empty((0,2))
    global d1
    
    for i in np.arange(0,r, .01):
        d1 = i
        count, mask = count_in_box(xs, ys, zs, length, width, height)
        c_hits= np.append(c_hits,[[d1,count]], axis = 0)
        # print(f"Trying d1 = {d1:.2f}, count = {count}")

        if time.time() - start_time > 10:
            print(f"Timed out at d1 = {d1}")
            raise TimeoutError("Was not able to solve within 10 seconds.")
    
    # Find the index of the maximum count (second column)
    max_hits = np.argmax(c_hits[:, 1])
    d1_opt = c_hits[max_hits, 0]  # Optimal d1
    max_count = c_hits[max_hits, 1]  # Corresponding count
    print(f"Optimal d1: {d1_opt}, count: {max_count}")

def count_in_cylinder(xs, ys, zs, x0,y0,z0, r, plength):
    # The cylinder is aligned along the x-axis
    x0, y0, z0 

    dx = xs - x0
    dy = ys - y0
    dz = zs - z0

    # Inside cylinder if radial distance in y-z plane is within radius
    radial_dist = np.sqrt(dy**2 + dz**2)
    inside_radial = radial_dist <= r

    # And x is within the cylinder's x-span
    inside_x = (dx >= 0) & (dx <= plength)

    inside = inside_radial & inside_x
    count = np.sum(inside)
    return count, inside

def opt2(r, xs,ys,zs,xop,yop,zop):
    count, mask = count_in_cylinder(xs, ys, zs, xop,yop,zop,r, plength=pmt_length)
    start_time = time.time()
    p_hits = np.empty((0,2))
    
    global d2
    
    for i in np.arange(0,r, .01):
        d2 = i
        count, mask = count_in_cylinder(xs, ys, zs, xop,yop,zop, r, plength=pmt_length)
        p_hits= np.append(p_hits,[[d2,count]], axis = 0)
        # print(f"Trying d1 = {d1:.2f}, count = {count}")

        if time.time() - start_time > 10:
            print(f"Timed out at d2 = {d2}")
            raise TimeoutError("Was not able to solve within 10 seconds.")
    
    # Find the index of the maximum count (second column)
    max_hits = np.argmax(p_hits[:, 1])
    d2_opt = p_hits[max_hits, 0]  # Optimal d1
    max_count = p_hits[max_hits, 1]  # Corresponding count
    print(f"Optimal d2: {d2_opt}, count: {max_count}")


def main():
    vari_all= np.empty((0,3))

    # Photon sphere
    xs, ys, zs = generate_sphere()
    sphere_bound_testing(xs, ys, zs)
    xs += 0 #sphere is aligned a 0
    ys += yo_c + width/2 # Align sphere with center of crystal
    zs += zo_c + height/2  # Mid-height of the box
    vari_all= np.append(vari_all, [[(R), (yo_c + width/2 + R), (zo_c + height/2 +R)]], axis = 0)
    vari_all= np.append(vari_all, [[(-R), (yo_c + width/2 -R), (zo_c + height/2 -R)]], axis = 0)

    # Crystal
    vari_all= np.append(vari_all, [[(xo_c+ length), yo_c, zo_c]], axis = 0)
    vari_all= np.append(vari_all, [[(xo_c+ length), yo_c+ width, zo_c+ height]], axis = 0)

    # PMT
    xop = -abs(d2)
    yop = yo_c + width/2 # Align sphere with center of crystal
    zop = zo_c + height/2  # Mid-height of the box
    vari_all = np.append(vari_all, [[xop -pmt_length, yop, zop]], axis=0)
    
    # model(xs, ys, zs, vari_all, xop, yop, zop)
    count, mask = count_in_box(xs, ys, zs, length, width, height)
    print(f"Photons inside the crystal: {count}/{len(xs)}")
    opt_1(R, xs,ys,zs)
    opt2(R, xs,ys,zs,xop,yop,zop) #Need to make graph of d1, d2, and hits
    # also time? Reflected points?? 
    

if __name__ == "__main__":
    main()
