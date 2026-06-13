from Vec3 import Vec3
from Mesh import Mesh

import math


class Tube(Mesh):

    def __init__(

        self,

        outer_radius=2,
        inner_radius=1,
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

            outer_x = outer_radius * c
            outer_z = outer_radius * s

            inner_x = inner_radius * c
            inner_z = inner_radius * s

            # OUTER TOP
            self.vertices.append(
                Vec3(outer_x, half_height, outer_z)
            )

            # INNER TOP
            self.vertices.append(
                Vec3(inner_x, half_height, inner_z)
            )

            # OUTER BOTTOM
            self.vertices.append(
                Vec3(outer_x, -half_height, outer_z)
            )

            # INNER BOTTOM
            self.vertices.append(
                Vec3(inner_x, -half_height, inner_z)
            )

        # ==========================================
        # FACES
        # ==========================================

        for i in range(segments):

            current = i * 4
            next_i = ((i + 1) % segments) * 4

            ot1 = current + 0
            it1 = current + 1
            ob1 = current + 2
            ib1 = current + 3

            ot2 = next_i + 0
            it2 = next_i + 1
            ob2 = next_i + 2
            ib2 = next_i + 3

            # ======================================
            # TOPO
            # ======================================

            self.faces.append((ot1, ot2, it1))
            self.faces.append((it1, ot2, it2))

            # ======================================
            # BASE
            # ======================================

            self.faces.append((ob1, ib1, ob2))
            self.faces.append((ib1, ib2, ob2))

            # ======================================
            # LATERAL EXTERNA
            # ======================================

            self.faces.append((ot1, ob1, ot2))
            self.faces.append((ot2, ob1, ob2))

            # ======================================
            # LATERAL INTERNA
            # ======================================

            self.faces.append((it1, it2, ib1))
            self.faces.append((it2, ib2, ib1))

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

        return f"Tube(vertices={len(self.vertices)}, faces={len(self.faces)})"