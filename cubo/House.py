from Vec3 import Vec3
from Mesh import Mesh

class House(Mesh):

    

    def __init__(self, size=1):

        super().__init__()

        half = size / 2

        # =====================
        # VÉRTICES
        # =====================

        self.vertices = [

            # CUBO
            Vec3(-half, -half, -half), # 0
            Vec3( half, -half, -half), # 1
            Vec3( half,  half, -half), # 2
            Vec3(-half,  half, -half), # 3

            Vec3(-half, -half,  half), # 4
            Vec3( half, -half,  half), # 5
            Vec3( half,  half,  half), # 6
            Vec3(-half,  half,  half), # 7

            # TELHADO (pirâmide)

            Vec3(-half, half, -half), # 8
            Vec3(-half, half,  half), # 9
            Vec3( half, half, -half), # 10
            Vec3( half, half,  half), # 11

            Vec3(0, size, 0),         # 12 topo
        ]

        # =====================
        # FACES
        # =====================

        self.faces = [

            # cubo

            (0,1,2), (0,2,3),
            (4,6,5), (4,7,6),

            (0,1,5), (0,5,4),
            (2,3,7), (2,7,6),

            (1,2,6), (1,6,5),
            (0,7,3), (0,4,7),

            # telhado

            (8,9,12),
            (9,11,12),
            (11,10,12),
            (10,8,12),
        ]

        self.face_colors = [

            # cubo
            (1,0,0),
            (1,0,0),

            (0,1,0),
            (0,1,0),

            (0,0,1),
            (0,0,1),

            (1,1,0),
            (1,1,0),

            (1,0,1),
            (1,0,1),

            (0,1,1),
            (0,1,1),

            # telhado
            (0.5,0.2,0.1),
            (0.5,0.2,0.1),
            (0.5,0.2,0.1),
            (0.5,0.2,0.1),
        ]

        self.compute_normals()

    def __repr__(self):

        return f"House(vertices={len(self.vertices)}, faces={len(self.faces)})"