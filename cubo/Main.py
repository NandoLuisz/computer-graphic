from House import House
from Renderer3D import Renderer3D

house = House(2)
house.rotate_x(45)

renderer = Renderer3D()

renderer.render_faces(house)