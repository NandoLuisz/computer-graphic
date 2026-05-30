# objeto: relizar um filtro, 
# selecionar apenas as faces que a camera consege ver

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

        center = (v0 + v1 + v2) / 3

        if np.dot(normal, -center) > 0:
            visible_faces.append(face)

    return visible_faces