from Vec3 import Vec3
from Mesh import Mesh


class Trapezoid(Mesh):

    def __init__(

        self,

        bottom_width=2,
        top_width=1,
        height=2,
        depth=1
    ):

        super().__init__()

        bw = bottom_width / 2
        tw = top_width / 2
        h = height / 2
        d = depth / 2

        # ==========================================
        # VÉRTICES
        # ==========================================

        self.vertices = [

            # frente
            Vec3(-bw, -h,  d), # 0
            Vec3( bw, -h,  d), # 1
            Vec3( tw,  h,  d), # 2
            Vec3(-tw,  h,  d), # 3

            # trás
            Vec3(-bw, -h, -d), # 4
            Vec3( bw, -h, -d), # 5
            Vec3( tw,  h, -d), # 6
            Vec3(-tw,  h, -d), # 7
        ]

        # ==========================================
        # FACES
        # ==========================================

        self.faces = [

            # frente
            (0,1,2),
            (0,2,3),

            # trás
            (4,6,5),
            (4,7,6),

            # esquerda
            (0,3,7),
            (0,7,4),

            # direita
            (1,5,6),
            (1,6,2),

            # topo
            (3,2,6),
            (3,6,7),

            # base
            (0,4,5),
            (0,5,1),
        ]

        # ==========================================
        # CORES
        # ==========================================

        self.face_colors = [

            (0.7, 0.3, 0.2)

            for _ in self.faces
        ]

        self.compute_normals()