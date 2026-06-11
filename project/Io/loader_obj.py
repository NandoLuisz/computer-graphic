import numpy as np
from geometry.face import Face

def load_obj(filename):

    vertices = []
    faces = []

    with open(filename, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            # vértices
            if parts[0] == "v":

                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])

                vertices.append([x, y, z])

            # faces
            elif parts[0] == "f":

                indices = []

                for token in parts[1:]:

                    # suporta:
                    # f 1 2 3
                    # f 1/1 2/2 3/3
                    # f 1//1 2//2 3//3

                    vertex_index = int(
                        token.split("/")[0]
                    ) - 1

                    indices.append(vertex_index)

                if len(indices) == 3:

                    faces.append(
                        Face(
                            tuple(indices),
                            (200,200,200)
                        )
                    )

                elif len(indices) == 4:

                    # quad -> 2 triângulos

                    faces.append(
                        Face(
                            (indices[0], indices[1], indices[2]),
                            (200,200,200)
                        )
                    )

                    faces.append(
                        Face(
                            (indices[0], indices[2], indices[3]),
                            (200,200,200)
                        )
                    )

    return (
        np.array(vertices, dtype=float),
        faces
    )