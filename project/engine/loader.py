from engine.face import Face
import numpy as np

def load_mesh(filename):

    vertices = []
    faces = []

    with open(filename, "r") as file:

        for line in file:

            parts = line.split()

            if not parts:
                continue

            if parts[0] == "v":

                vertices.append([
                    float(parts[1]), # x
                    float(parts[2]), # y
                    float(parts[3]) # z
                ])

            elif parts[0] == "f":

                face = Face(
                   
                    vertices= ( 
                        int(parts[1])-1, 
                        int(parts[2])-1,
                        int(parts[3])-1
                    ),
                    color=(200,200,200),
                )

                faces.append(face)

    return np.array(vertices), faces

def build_edges(faces):
    edges = set()

    for face in faces:
        
        a,b,c = face.vertices

        edges.add(tuple(sorted((a,b))))
        edges.add(tuple(sorted((b,c))))
        edges.add(tuple(sorted((c,a))))
        
    return list(edges)

