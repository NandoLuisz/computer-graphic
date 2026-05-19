from Cube import Cube
from Renderer3D import Renderer3D

cube = Cube(2)
cube.scale(1, 4, 1)
cube.translate(10, 2, 0)
cube.rotate_x(45)

renderer = Renderer3D()

renderer.render_wireframe(cube)
