import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Renderer3D:


    def setup_axis(self, ax, limit=3):

        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.set_box_aspect([1,1,1])


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

            ax.plot(xs, ys, zs, color='black')

        # =========================
        # NORMAIS
        # =========================

        for i, face in enumerate(mesh.faces):

            v1 = mesh.vertices[face[0]]
            v2 = mesh.vertices[face[1]]
            v3 = mesh.vertices[face[2]]

            center = (v1 + v2 + v3) / 3

            normal = mesh.normals[i]

            ax.quiver(

                center.x,
                center.y,
                center.z,

                normal.x,
                normal.y,
                normal.z,

                length=0.3,
                color='red'
            )

        self.setup_axis(ax)

        plt.show()


    def render_faces(self, mesh):

        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        self.render_faces_on_axis(ax, mesh)

        self.setup_axis(ax)

        plt.show()


    def render_faces_on_axis(self, ax, mesh):

        triangles = []

        for face in mesh.faces:

            triangle = [

                mesh.vertices[face[0]].to_tuple(),
                mesh.vertices[face[1]].to_tuple(),
                mesh.vertices[face[2]].to_tuple(),
            ]

            triangles.append(triangle)

        # evita erro do matplotlib
        if len(triangles) == 0:
            return

        collection = Poly3DCollection(

            triangles,

            facecolors=mesh.face_colors,

            edgecolors='black',

            linewidths=1,

            alpha=0.8
        )

        ax.add_collection3d(collection)