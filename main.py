import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from solids import create_cube

cube = create_cube()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

triangles = []

for face in cube.faces:

    triangle = [
        cube.vertices[face[0]],
        cube.vertices[face[1]],
        cube.vertices[face[2]]
    ]

    triangles.append(triangle)

collection = Poly3DCollection(
    triangles,
    facecolors='cyan',
    edgecolors='black',
    alpha=0.8
)

ax.add_collection3d(collection)

ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_zlim(-2,2)

plt.show()