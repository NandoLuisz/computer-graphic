from Vec3 import Vec3
from Mesh import Mesh


class Box(Mesh):

    def __init__(

        self,

        width=1,
        height=1,
        depth=1
    ):

        super().__init__()

        hw = width / 2
        hh = height / 2
        hd = depth / 2

        # ==================================
        # VÉRTICES
        # ==================================

        self.vertices = [

            # frente
            Vec3(-hw, -hh,  hd), # 0
            Vec3( hw, -hh,  hd), # 1
            Vec3( hw,  hh,  hd), # 2
            Vec3(-hw,  hh,  hd), # 3

            # trás
            Vec3(-hw, -hh, -hd), # 4
            Vec3( hw, -hh, -hd), # 5
            Vec3( hw,  hh, -hd), # 6
            Vec3(-hw,  hh, -hd), # 7
        ]

        # ==================================
        # FACES
        # ==================================

        self.faces = [

            # frente
            (0,1,2),
            (0,2,3),

            # trás
            (5,4,7),
            (5,7,6),

            # esquerda
            (4,0,3),
            (4,3,7),

            # direita
            (1,5,6),
            (1,6,2),

            # topo
            (3,2,6),
            (3,6,7),

            # baixo
            (4,5,1),
            (4,1,0),
        ]

        # ==================================
        # CORES
        # ==================================

        self.face_colors = [

            (1, 0, 0)

            for _ in self.faces
        ]

        self.compute_normals()

    def __repr__(self):

        return (

            f"Box("
            f"vertices={len(self.vertices)}, "
            f"faces={len(self.faces)})"
        )