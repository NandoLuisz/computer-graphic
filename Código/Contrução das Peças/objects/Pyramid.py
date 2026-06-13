from Vec3 import Vec3
from Mesh import Mesh

class Pyramid(Mesh):

    def __init__(self, size=1):

        super().__init__()

        half = size / 2

        self.vertices = [

            Vec3(-half, -half, -half), # 0
            Vec3(-half, -half,  half), # 1
            Vec3( half, -half, -half), # 2
            Vec3( half, -half,  half), # 3

            Vec3(0, half, 0),          # 4 topo
        ]

        self.faces = [

            (0,1,4),
            (1,3,4),
            (3,2,4),
            (2,0,4),

            (0,2,1),
            (1,2,3),
        ]

        self.compute_normals()

    def __repr__(self):

        return f"Pyramid(vertices={self.vertices}, faces={self.faces})"