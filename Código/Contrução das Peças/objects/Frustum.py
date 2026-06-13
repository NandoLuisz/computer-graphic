from Vec3 import Vec3
from Mesh import Mesh

import math

class Frustum(Mesh):

    def __init__(

        self,

        bottom_radius=2,
        top_radius=1,
        height=2,
        segments=32
    ):

        super().__init__()

        half_height = height / 2

        # ==========================================
        # VÉRTICES
        # ==========================================

        for i in range(segments):

            angle = (2 * math.pi * i) / segments

            c = math.cos(angle)
            s = math.sin(angle)

            # base
            bx = bottom_radius * c
            bz = bottom_radius * s

            # topo
            tx = top_radius * c
            tz = top_radius * s

            # topo
            self.vertices.append(

                Vec3(
                    tx,
                    half_height,
                    tz
                )
            )

            # base
            self.vertices.append(

                Vec3(
                    bx,
                    -half_height,
                    bz
                )
            )

        # ==========================================
        # FACES LATERAIS
        # ==========================================

        for i in range(segments):

            current = i * 2

            next_i = ((i + 1) % segments) * 2

            top1 = current
            bottom1 = current + 1

            top2 = next_i
            bottom2 = next_i + 1

            # triângulo 1
            self.faces.append(

                (
                    top1,
                    bottom1,
                    top2
                )
            )

            # triângulo 2
            self.faces.append(

                (
                    top2,
                    bottom1,
                    bottom2
                )
            )

        # ==========================================
        # CORES
        # ==========================================

        self.face_colors = [

            (1, 0.0, 0.0)

            for _ in self.faces
        ]

        # ==========================================
        # NORMAIS
        # ==========================================

        self.compute_normals()

    def __repr__(self):

        return f"Frustum(vertices={len(self.vertices)}, faces={len(self.faces)})"