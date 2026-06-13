from Vec3 import Vec3
from Mesh import Mesh

import math


class Torus(Mesh):

    def __init__(

        self,

        major_radius=1,
        minor_radius=0.25,

        major_segments=64,
        minor_segments=32
    ):

        super().__init__()

        # ==========================================
        # VÉRTICES
        # ==========================================

        for i in range(major_segments):

            u = (2 * math.pi * i) / major_segments

            for j in range(minor_segments):

                v = (2 * math.pi * j) / minor_segments

                x = (

                    major_radius +
                    minor_radius * math.cos(v)

                ) * math.cos(u)

                y = minor_radius * math.sin(v)

                z = (

                    major_radius +
                    minor_radius * math.cos(v)

                ) * math.sin(u)

                self.vertices.append(

                    Vec3(x, y, z)
                )

        # ==========================================
        # FACES
        # ==========================================

        for i in range(major_segments):

            for j in range(minor_segments):

                current = i * minor_segments + j

                next_j = (

                    i * minor_segments +
                    (j + 1) % minor_segments
                )

                next_i = (

                    ((i + 1) % major_segments)
                    * minor_segments + j
                )

                next_i_next_j = (

                    ((i + 1) % major_segments)
                    * minor_segments +

                    (j + 1) % minor_segments
                )

                # triângulo 1
                self.faces.append(

                    (
                        current,
                        next_i,
                        next_j
                    )
                )

                # triângulo 2
                self.faces.append(

                    (
                        next_j,
                        next_i,
                        next_i_next_j
                    )
                )

        # ==========================================
        # CORES
        # ==========================================

        self.face_colors = [

            (1, 0, 0)

            for _ in self.faces
        ]

        # ==========================================
        # NORMAIS
        # ==========================================

        self.compute_normals()

    def __repr__(self):

        return (

            f"Torus(vertices={len(self.vertices)}, "
            f"faces={len(self.faces)})"
        )