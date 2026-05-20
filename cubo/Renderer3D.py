import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Renderer3D:


    def setup_axis(self, ax, mesh, margin=1):

        xs = [v.x for v in mesh.vertices]
        ys = [v.y for v in mesh.vertices]
        zs = [v.z for v in mesh.vertices]

        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - margin, max(ys) + margin)
        ax.set_zlim(min(zs) - margin, max(zs) + margin)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        dz = max(zs) - min(zs)

        # evita dimensão zero
        if dx == 0:
            dx = 1

        if dy == 0:
            dy = 1

        if dz == 0:
            dz = 1

        ax.set_box_aspect([dx, dy, dz])


    # ==========================================
    # WIREFRAME
    # ==========================================

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

        # ==========================================
        # NORMAIS
        # ==========================================

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

        self.setup_axis(ax, mesh)

        plt.show()


    # ==========================================
    # FACES PREENCHIDAS
    # ==========================================

    def render_faces(self, mesh):

        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        self.render_faces_on_axis(ax, mesh)

        self.setup_axis(ax, mesh)

        plt.show()


    # ==========================================
    # RENDER EM UM AXIS EXISTENTE
    # ==========================================

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

        # fallback de cores
        if hasattr(mesh, "face_colors"):

            colors = mesh.face_colors

        else:

            colors = [(0.7, 0.7, 0.7)] * len(mesh.faces)

        collection = Poly3DCollection(

            triangles,

            facecolors=colors,

            edgecolors=None,

            linewidths=0,

            alpha=1
        )

        ax.add_collection3d(collection)