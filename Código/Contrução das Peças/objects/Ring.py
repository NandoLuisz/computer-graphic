from Vec3 import Vec3
from Mesh import Mesh

import math


class Ring(Mesh):

    def __init__(

        self,

        outer_radius=2,
        inner_radius=1,
        segments=32
    ):

        super().__init__()

        # ==========================================
        # VÉRTICES
        # ==========================================

        for i in range(segments):

            angle = (2 * math.pi * i) / segments

            c = math.cos(angle)
            s = math.sin(angle)

            # externo
            outer_x = outer_radius * c
            outer_z = outer_radius * s

            # interno
            inner_x = inner_radius * c
            inner_z = inner_radius * s

            self.vertices.append(
                Vec3(outer_x, 0, outer_z)
            )

            self.vertices.append(
                Vec3(inner_x, 0, inner_z)
            )

        # ==========================================
        # FACES
        # ==========================================

        for i in range(segments):

            current_outer = i * 2
            current_inner = i * 2 + 1

            next_outer = ((i + 1) % segments) * 2
            next_inner = ((i + 1) % segments) * 2 + 1

            # triângulo 1
            self.faces.append(

                (
                    current_outer,
                    next_outer,
                    current_inner
                )
            )

            # triângulo 2
            self.faces.append(

                (
                    current_inner,
                    next_outer,
                    next_inner
                )
            )

        # ==========================================
        # CORES
        # ==========================================

        self.face_colors = [

            (0.8, 0.6, 0.2)

            for _ in self.faces
        ]

        # ==========================================
        # NORMAIS
        # ==========================================

        self.compute_normals()

    def __repr__(self):

        return f"Ring(vertices={len(self.vertices)}, faces={len(self.faces)})"