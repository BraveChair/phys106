import plotly.graph_objects as go
import numpy as np
from numpy import pi, sin, cos
from scipy.spatial.transform import Rotation as Rot

np.random.seed(2022)
deg2radians= lambda deg: deg*pi/180
def spheric2cartesian(r, theta, phi):
    x = r*cos(theta) *sin(phi)
    y = r*sin(theta)*sin(phi)
    z= r*cos(phi)
    return x, y, z

R = 1.5
theta_m = 15   
theta_M = theta_m + 40
phi_m= 70    
phi_M=  phi_m +50
 

thetar_m, thetar_M = deg2radians(theta_m), deg2radians(theta_M)
phir_m, phir_M = deg2radians(phi_m), deg2radians(phi_M)

colorscale=[[0, "lightblue"],[1, "lightblue"]]

r_plus =0.1  #a small amount to be added to the radius
t_plus=0.05  # to be substracted/added to thetar and phir to avoid points  lying on the sector of coordinates

#define the circular sector under the scatter points, i.e. equivalent to the plane z=cst for cartesian axes
r = np.linspace(0, R+r_plus, 100)
theta = np.linspace(thetar_m-t_plus, thetar_M+t_plus, 50)
rm, theta = np.meshgrid(r, theta)
phi = (phir_M+t_plus)*np.ones(rm.shape)
xb, yb, zb = spheric2cartesian(rm, theta, phi)

lighting =dict(ambient=0.8,
               diffuse=0.8,
               specular=0.2,
               roughness=0.5,
               fresnel=0.4)
lightposition =dict(x=1000, y=1000, z=-1000)
fig=go.Figure(go.Surface(x=xb, y=yb, z=zb, coloraxis="coloraxis", 
                         lighting=lighting,
                        lightposition=lightposition)) #The floor of the plot

#plot the sector, equivalent to the plane behind the points  in cartesian axes
Phi = np.linspace(phir_m-t_plus, phir_M+t_plus, 75)
rp, Phi =np.meshgrid(r, Phi)
Theta = (thetar_M+t_plus)*np.ones(rp.shape)
xb, yb, zb = spheric2cartesian(rp, Theta, Phi)
fig.add_surface(x=xb, y=yb, z=zb, 
                coloraxis="coloraxis",
                lighting=lighting,
               lightposition=lightposition)

#####
#Generate points to be ploted with respect to spheric layout
n=250
rp = R*np.random.rand(n)
thetap = thetar_m + (thetar_M-thetar_m) *np.random.rand(n)
phip= phir_m +(phir_M-phir_m)* np.random.rand(n)
X, Y, Z = spheric2cartesian (rp, thetap, phip)

fig.add_scatter3d(x=X, y=Y, z=Z, mode="markers", 
                  marker_size=3, marker_color="RoyalBlue")
# grid lines on the floor sector:
thetagr = deg2radians(np.asarray([15, 25, 35, 45]))
XL = []
YL = []
ZL = []
for t in thetagr:
    xl, yl, zl =spheric2cartesian(np.linspace(0, R+r_plus, 10), t, phir_M+t_plus)               
    XL.extend(list(xl))
    XL.append(None)
    YL.extend(list(yl)) 
    YL.append(None)
    ZL.extend(list(zl))  
    ZL.append(None)
rgr  =[0.5, 1, 1.5]    
for rg in rgr:
    xl, yl, zl =spheric2cartesian( rg,  np.linspace(thetar_m-t_plus, thetar_M+t_plus, 30), (phir_M+t_plus)*np.ones(30))
    XL.extend(list(xl))
    XL.append(None)
    YL.extend(list(yl)) 
    YL.append(None)
    ZL.extend(list(zl))  
    ZL.append(None)
fig.add_scatter3d(x=XL, y=YL, z=ZL, mode="lines", line_color="rgb(200, 200, 200)", line_width=3) 
    
# grid Lines on the back sector:
phigr = deg2radians(np.asarray([75, 85, 95, 105, 115]))
XL = []
YL = []
ZL = []
for p in phigr:
    xl, yl, zl =spheric2cartesian(np.linspace(0, R+r_plus, 10), thetar_M+t_plus, p)               
    XL.extend(list(xl))
    XL.append(None)
    YL.extend(list(yl)) 
    YL.append(None)
    ZL.extend(list(zl))  
    ZL.append(None)
for rg in rgr:
    xl, yl, zl =spheric2cartesian( rg, (thetar_M+t_plus)*np.ones(30), np.linspace(phir_m-t_plus, phir_M+t_plus, 30))
    XL.extend(list(xl))
    XL.append(None)
    YL.extend(list(yl)) 
    YL.append(None)
    ZL.extend(list(zl))  
    ZL.append(None)
fig.add_scatter3d(x=XL, y=YL, z=ZL, mode="lines", line_color="rgb(200, 200, 200)", line_width=3) 


fig.update_layout(width=800, height=800, 
                  showlegend=False,
                  coloraxis=dict(colorscale=colorscale, showscale=False),
                  scene =dict(aspectmode="data",
                              xaxis_visible=False, 
                              yaxis_visible=False, zaxis_visible=False,
                              camera_eye=dict(x=1.85, y=-1.85, z=0.8))) 
fig.show()