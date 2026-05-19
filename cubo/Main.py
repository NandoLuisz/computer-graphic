from Cube import Cube
from Renderer3D import Renderer3D

cube = Cube(2)
cube.scale(1.5, 2, 2.5)

renderer = Renderer3D()

renderer.render_wireframe(cube)
