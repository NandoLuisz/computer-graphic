from Vec3 import Vec3
from Mesh import Mesh
from Mat4 import Mat4

class Cube(Mesh):
    def __init__(self, size=1):
        super().__init__()
        half = size / 2
        self.vertices = [
            Vec3(-half, -half, -half), # 0
            Vec3(half, -half, -half),  # 1
            Vec3(half, half, -half),   # 2
            Vec3(-half, half, -half),  # 3
            Vec3(-half, -half, half),  # 4
            Vec3(half, -half, half),   # 5
            Vec3(half, half, half),    # 6
            Vec3(-half, half, half)    # 7
        ]
        self.faces = [
            (0, 1, 2), (0, 2, 3), # Back face
            (4, 6, 5), (4, 7, 6), # Front face
            (0, 1, 5), (0, 5, 4), # Bottom face
            (2, 3, 7), (2, 7, 6), # Top face
            (1, 2, 6), (1, 6, 5), # Right face
            (0, 7, 3), (0, 4, 7)  # Left face
        ]
        self.compute_normals()

    def __repr__(self):
        return f"Cube(size={self.vertices[1].x * 2}, vertices={self.vertices}, faces={self.faces}, normals={self.normals}, color={self.color})"