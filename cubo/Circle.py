from Vec3 import Vec3
from Mesh import Mesh

import math


class Circle(Mesh):

    def __init__(self, radius=1, segments=64):

        super().__init__()

        # ==========================================
        # CENTRO
        # ==========================================

        self.vertices.append(
            Vec3(0,0,0)
        )

        # ==========================================
        # BORDA
        # ==========================================

        for i in range(segments):

            angle = (2 * math.pi * i) / segments

            x = radius * math.cos(angle)
            z = radius * math.sin(angle)

            self.vertices.append(
                Vec3(x, 0, z)
            )

        # ==========================================
        # TRIÂNGULOS
        # ==========================================

        for i in range(1, segments):

            self.faces.append(
                (0, i, i + 1)
            )

        # fecha último triângulo
        self.faces.append(
            (0, segments, 1)
        )

        # ==========================================
        # CORES
        # ==========================================

        self.face_colors = [

            (0.2, 0.2, 0.8)

            for _ in self.faces
        ]

        # ==========================================
        # NORMAIS
        # ==========================================

        self.compute_normals()