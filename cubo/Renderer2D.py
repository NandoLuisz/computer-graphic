import matplotlib.pyplot as plt

class Renderer:

    def render_wireframe(self, mesh):

        for face in mesh.faces:

            v0 = mesh.vertices[face[0]]
            v1 = mesh.vertices[face[1]]
            v2 = mesh.vertices[face[2]]

            points = [v0, v1, v2, v0]

            xs = [p.x for p in points]
            ys = [p.y for p in points]

            plt.plot(xs, ys)

        plt.axis('equal')
        plt.show()