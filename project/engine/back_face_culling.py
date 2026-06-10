# objeto: relizar um filtro, 
# selecionar apenas as faces que a camera consege ver

import numpy as np

import numpy as np

def back_face(faces, vertices):

    visible_faces = []

    for face in faces:

        v0 = vertices[face.vertices[0]]
        v1 = vertices[face.vertices[1]]
        v2 = vertices[face.vertices[2]]

        edge1 = v1 - v0
        edge2 = v2 - v0

        normal = np.cross(edge1, edge2)

        norm = np.linalg.norm(normal)

        if norm < 1e-6:
            continue

        normal /= norm

        center = (v0 + v1 + v2) / 3.0

        face.normal = normal
        face.center = center

        face.depth = (
            v0[2] +
            v1[2] +
            v2[2]
        ) / 3.0

        if np.dot(normal, -center) > 0:
            visible_faces.append(face)

    return visible_faces
