import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to convert spherical to Cartesian coordinates
def spheric2cartesian(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

# Parameters
R = 1  # Radius of the sphere
n = 1000  # Number of random points

# Generate random angles (Full sphere)
thetap_full = np.arccos(1 - 2 * np.random.rand(n))  # Theta: 0 to π
phip_full =  2* np.pi * np.random.rand(n) #n  # Phi: 0 to 2π  


# Convert spherical coordinates to Cartesian
X_full, Y_full, Z_full = spheric2cartesian(R, thetap_full, phip_full)

# Set up the figure and 3D axis
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the random points on the sphere
ax.scatter(X_full, Y_full, Z_full, color="royalblue", s=3, alpha=0.8)

# Wireframe: Equator (phi = π/2)
theta_eq = np.pi / 2
phi_eq = np.linspace(0, 2 * np.pi, 100)  # Equator circle
X_eq, Y_eq, Z_eq = spheric2cartesian(R, theta_eq, phi_eq)
ax.plot(X_eq, Y_eq, Z_eq, color="red", lw=2)

# Set labels and aspect ratio
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set equal aspect ratio for all axes
ax.set_box_aspect([1, 1, 1])

# Set title
ax.set_title('Sphere with Equator Border')

# Show the plot
plt.show()