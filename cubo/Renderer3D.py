import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Renderer3D:

    def render_wireframe(self, mesh):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for face in mesh.faces:

            v0 = mesh.vertices[face[0]]
            v1 = mesh.vertices[face[1]]
            v2 = mesh.vertices[face[2]]

            triangle = [v0, v1, v2, v0]

            xs = [v.x for v in triangle]
            ys = [v.y for v in triangle]
            zs = [v.z for v in triangle]

            ax.plot(xs, ys, zs)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.set_box_aspect([1,1,1])

        plt.show()