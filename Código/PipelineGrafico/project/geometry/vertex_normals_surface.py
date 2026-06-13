import numpy as np

def compute_vertex_normals(vertices, faces):

    normals = np.zeros(
        (len(vertices), 3),
        dtype=float
    )

    for face in faces:

        i0, i1, i2 = face.vertices

        v0 = vertices[i0]
        v1 = vertices[i1]
        v2 = vertices[i2]

        edge1 = v2 - v0
        edge2 = v1 - v0

        face_normal = np.cross( edge1, edge2 ).astype(float)

        norm = np.linalg.norm(face_normal)

        if norm < 1e-6:
            continue

        face_normal /= norm

        normals[i0] += face_normal
        normals[i1] += face_normal
        normals[i2] += face_normal

    for i in range(len(normals)):

        norm = np.linalg.norm(normals[i])

        if norm > 1e-6:
            normals[i] /= norm

    return normals