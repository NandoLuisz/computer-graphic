from Vec3 import Vec3
from Mesh import Mesh

import math


class LatheMesh(Mesh):

    def __init__(

        self,

        profile_points,

        segments=64
    ):

        super().__init__()

        # ======================================
        # VÉRTICES
        # ======================================

        for i in range(segments):

            angle = (2 * math.pi * i) / segments

            c = math.cos(angle)
            s = math.sin(angle)

            for radius, y in profile_points:

                x = radius * c
                z = radius * s

                self.vertices.append(

                    Vec3(x, y, z)
                )

        # ======================================
        # FACES
        # ======================================

        profile_count = len(profile_points)

        for i in range(segments):

            next_i = (i + 1) % segments

            for j in range(profile_count - 1):

                current = i * profile_count + j

                next_ring = next_i * profile_count + j

                current_top = current + 1
                next_ring_top = next_ring + 1

                # triângulo 1
                self.faces.append(

                    (
                        current,
                        next_ring,
                        current_top
                    )
                )

                # triângulo 2
                self.faces.append(

                    (
                        current_top,
                        next_ring,
                        next_ring_top
                    )
                )

        # ======================================
        # CORES
        # ======================================

        self.face_colors = [

            (1, 0, 0)

            for _ in self.faces
        ]

        self.compute_normals()