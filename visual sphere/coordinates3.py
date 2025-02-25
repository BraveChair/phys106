import plotly.graph_objects as go
import numpy as np
from numpy import pi, sin, cos, sqrt

# Convert spherical to Cartesian
def spheric2cartesian(r, theta, phi):
    x = r * cos(theta) * sin(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(phi)
    return x, y, z

# Define parameters
R = 1  # Sphere radius
n = 1000  # Number of points

# Generate random points in spherical coordinates (uniformly distributed in 3D)

rd = R * np.cbrt(np.random.rand(n))  # Cube root for uniform sphere distribution
thetap = pi * np.random.rand(n)  # Theta: 0 to 2π
phip = np.arccos(1 - 2 * np.random.rand(n))  # Phi: Corrected for uniform sampling

# Convert to Cartesian
X, Y, Z = spheric2cartesian(rd, thetap, phip)

# Create scatter plot
fig = go.Figure()
fig.add_scatter3d(x=X, y=Y, z=Z, mode="markers",
                  marker=dict(size=3, color="RoyalBlue", opacity=0.8))

# Set layout
fig.update_layout(width=800, height=800,
                  showlegend=False,
                  scene=dict(aspectmode="data",
                             xaxis=dict(visible=False),
                             yaxis=dict(visible=False),
                             zaxis=dict(visible=False),
                             camera_eye=dict(x=1.5, y=-1.5, z=1)))

# Show plot
fig.show()
