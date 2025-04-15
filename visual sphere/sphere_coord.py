import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
R = 1  # Radius of the sphere
n = 10000  # Number of random points
epsilon = np.finfo(float).eps
alpha_s = .8

# Function to convert spherical to Cartesian coordinates
def spheric2cartesian(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

def generate_sphere():
    # Generate random angles (Full sphere)
    thetap_full = np.arccos(1 - 2 * np.random.rand(n))  # Theta: 0 to π
    phip_full =  2* np.pi * np.random.rand(n) #n  # Phi: 0 to 2π  

    # Convert spherical coordinates to Cartesian
    X_full, Y_full, Z_full = spheric2cartesian(R, thetap_full, phip_full)

    # Set up the figure and 3D axis
    return X_full,Y_full,Z_full

def show_sphere(X_full, Y_full, Z_full,): # Plot the random points on the sphere
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X_full, Y_full, Z_full, color="royalblue", s=3, alpha= alpha_s)
    
    # Set labels and aspect ratio
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set equal aspect ratio for all axes
    # ax.set_box_aspect([1, 1, 1])
    ax.set_title('Monte Carlo Sphere')
    plt.show()

def sphere_bound_testing(X_full, Y_full, Z_full):
    coords = np.vstack([X_full, Y_full, Z_full])
    bad_points = np.any((coords < -R - epsilon) | (coords > R + epsilon), axis = 0)
    if np.any(bad_points):
        print("Bad Coordinates: ", coords[:,bad_points[1]])
        raise ValueError("DATA ERROR: Some points are outside the sphere bounds.")
    else: print("All points within bounds!")

def main():
    X_full,Y_full,Z_full = generate_sphere()
    sphere_bound_testing(X_full,Y_full,Z_full)
    # show_sphere(X_full,Y_full,Z_full)

if __name__ == "__main__":
    main()