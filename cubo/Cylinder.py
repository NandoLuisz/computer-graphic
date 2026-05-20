from Vec3 import Vec3
from Mesh import Mesh

import math

class Cylinder(Mesh):

    def __init__(self, radius=1, height=1, segments=32):

        super().__init__()

        half_height = height / 2
        top_center = 0
        bottom_center = 1

        self.vertices.append(
            Vec3(0, half_height, 0)
        )

        self.vertices.append(
            Vec3(0, -half_height, 0)
        )
        for i in range(segments):

            angle = (2 * math.pi * i) / segments

            x = radius * math.cos(angle)
            z = radius * math.sin(angle)

            # topo
            self.vertices.append(
                Vec3(x, half_height, z)
            )

            # base
            self.vertices.append(
                Vec3(x, -half_height, z)
            )
        for i in range(segments):

            top1 = 2 + i * 2
            bottom1 = top1 + 1

            top2 = 2 + ((i + 1) % segments) * 2
            bottom2 = top2 + 1

            # topo
            self.faces.append(
                (top_center, top1, top2)
            )

            # base
            self.faces.append(
                (bottom_center, bottom2, bottom1)
            )

            # lateral triângulo 1
            self.faces.append(
                (top1, bottom1, top2)
            )

            # lateral triângulo 2
            self.faces.append(
                (top2, bottom1, bottom2)
            )
        self.face_colors = [

            (0.0, 0.0, 0.0)

            for _ in self.faces
        ]
        self.compute_normals()