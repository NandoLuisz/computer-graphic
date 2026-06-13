from Vec3 import Vec3
from Mesh import Mesh

import math


class Sphere(Mesh):

    def __init__(

        self,

        radius=1,

        stacks=16,

        sectors=32
    ):

        super().__init__()

        # ==========================================
        # VÉRTICES
        # ==========================================

        for i in range(stacks + 1):

            phi = math.pi * i / stacks

            for j in range(sectors):

                theta = 2 * math.pi * j / sectors

                x = radius * math.sin(phi) * math.cos(theta)

                y = radius * math.cos(phi)

                z = radius * math.sin(phi) * math.sin(theta)

                self.vertices.append(
                    Vec3(x, y, z)
                )

        # ==========================================
        # FACES
        # ==========================================

        for i in range(stacks):

            for j in range(sectors):

                current = i * sectors + j

                next_sector = i * sectors + (j + 1) % sectors

                next_stack = (i + 1) * sectors + j

                next_stack_next_sector = (

                    (i + 1) * sectors +
                    (j + 1) % sectors
                )

                # triângulo 1
                self.faces.append(

                    (
                        current,
                        next_stack,
                        next_sector
                    )
                )

                # triângulo 2
                self.faces.append(

                    (
                        next_sector,
                        next_stack,
                        next_stack_next_sector
                    )
                )

        # ==========================================
        # CORES
        # ==========================================

        self.face_colors = [

            (1, 0.0, 0.0)

            for _ in self.faces
        ]

        self.compute_normals()