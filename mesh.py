import numpy as np

class Mesh:
    def __init__(self, vertices, faces, color=(1, 1, 1)):
        self.vertices = np.array(vertices, dtype=float)
        self.faces = np.array(faces, dtype=int)

        self.color = color

        self.normals = self.compute_face_normals()

    def compute_face_normals(self):

        normals = []

        for face in self.faces:

            v1 = self.vertices[face[0]]
            v2 = self.vertices[face[1]]
            v3 = self.vertices[face[2]]

            edge1 = v2 - v1
            edge2 = v3 - v1

            normal = np.cross(edge1, edge2)

            norm = np.linalg.norm(normal)

            if norm != 0:
                normal = normal / norm

            normals.append(normal)

        return np.array(normals)