import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Cylinder parameters
radius = 1
height = 2
num_points = 50

# Generate cylinder data
theta = np.linspace(0, 2*np.pi, num_points)
z = np.linspace(0, height, num_points)
theta, z = np.meshgrid(theta, z)
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Create the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the cylinder surface
ax.plot_surface(x, y, z)

# Plot the top and bottom caps
z_top = np.full((num_points, num_points), height)
z_bottom = np.zeros((num_points, num_points))
ax.plot_surface(x, y, z_top)
ax.plot_surface(x, y, z_bottom)

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set title
ax.set_title('Closed Cylinder')

# Show the plot
plt.show()

def rotate_points(x, y, z, R):
    # Flatten and stack coordinates (N points x 3)
    coords = np.vstack((x.flatten(), y.flatten(), z.flatten()))
    # Apply rotation
    rotated = R @ coords
    # Reshape back to original grid shape
    shape = x.shape
    return rotated[0].reshape(shape), rotated[1].reshape(shape), rotated[2].reshape(shape)

def rotation_matrix(axis, angle_deg):
    angle = np.radians(angle_deg)
    if axis == 'x':
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ])
    elif axis == 'y':
        return np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ])
    elif axis == 'z':
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ])
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")