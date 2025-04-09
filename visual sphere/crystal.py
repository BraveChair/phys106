import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection



# Parameters
length, width, height = 2.05, 2.05, 20
d1 = 1
x_pos, y_pos, z_pos = d1, 0, 0

def make_box():
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
    
    # Create a Poly3DCollection for all the triangles with blue cube color
    poly3d = Poly3DCollection([vertices[triangle] for triangle in triangles], color='black', alpha=0.3)
    return poly3d
    

def show_box(poly):
    # Plot the cuboid
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(poly)

    # Set background color 
    ax.set_facecolor('Cyan')
    
    ax.set_axis_off()
    ax.set_box_aspect([length, width, height])

    plt.show()

def main():
    poly = make_box()
    show_box(poly)

if __name__ == "__main__":
    main()