from matplotlib.patches import Circle

from House import House
from Renderer3D import Renderer3D
from Circle import Circle
from Cylinder import Cylinder

house = House(2)
circle = Circle()
cylinder = Cylinder() #dama
renderer = Renderer3D()

renderer.render_faces(cylinder)