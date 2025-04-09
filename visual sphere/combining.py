import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- Utility Functions ---
from sphere_coord import generate_sphere, show_sphere, sphere_bound_testing

def draw_box():
    # Crystal dimensions 
    length, width, height = 2.05, 2.05, 20
    x_pos, y_pos, z_pos = 1, 0, 0

    # Define the vertices of the cuboid
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

    # Define the list of faces (each face is a quadrilateral, split into two triangles)
    faces = [
        [0, 1, 2, 3],  # bottom
        [4, 5, 6, 7],  # top
        [0, 1, 5, 4],  # front
        [1, 2, 6, 5],  # right
        [2, 3, 7, 6],  # back
        [3, 0, 4, 7]   # left
    ]

    # Split each quadrilateral face into two triangles
    triangles = []
    for face in faces:
        # The face is a quadrilateral, split into two triangles
        triangles.append([face[0], face[1], face[2]])
        triangles.append([face[0], face[2], face[3]])

    # Plot the cuboid
    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')

    # Create a Poly3DCollection for all the triangles with blue cube color
    poly3d = Poly3DCollection([vertices[triangle] for triangle in triangles], color='black', alpha=0.7)
    ax.add_collection3d(poly3d)

    # Set background color 
    ax.set_facecolor('Cyan')

    ax.set_axis_off()
    ax.set_box_aspect([length, width, height])

    
plt.show()
