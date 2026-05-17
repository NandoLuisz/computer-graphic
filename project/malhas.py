import numpy as np

class Mesh:
    def __init__(self, vertices, faces, color):
        self.vertices = np.array(vertices, dtype=float)  # Matriz Nx4
        self.faces = np.array(faces, dtype=int)          # Matriz Fx3
        self.color = np.array(color, dtype=float)        # RGB [0.0, 1.0]
        self.normals = []                                # Normais por face
        self.compute_normals()

    def compute_normals(self):
        normals = []
        for face in self.faces:
            v0 = self.vertices[face[0]][:3]
            v1 = self.vertices[face[1]][:3]
            v2 = self.vertices[face[2]][:3]
            
            edge1 = v1 - v0
            edge2 = v2 - v0
            
            # Produto vetorial para obter a normal geométrica da face
            n = np.cross(edge1, edge2)
            norm = np.linalg.norm(n)
            if norm > 0:
                n = n / norm
            normals.append(n)
        self.normals = np.array(normals)

def create_cube(color=[0.2, 0.7, 0.3]):
    # 8 Vértices locais do cubo (Aresta 2, centrado na origem)
    vertices = np.array([
        [-1.0, -1.0, -1.0,  1.0], # 0
        [ 1.0, -1.0, -1.0,  1.0], # 1
        [ 1.0,  1.0, -1.0,  1.0], # 2
        [-1.0,  1.0, -1.0,  1.0], # 3
        [-1.0, -1.0,  1.0,  1.0], # 4
        [ 1.0, -1.0,  1.0,  1.0], # 5
        [ 1.0,  1.0,  1.0,  1.0], # 6
        [-1.0,  1.0,  1.0,  1.0]  # 7
    ], dtype=float)

    # 12 Triângulos mapeados em sentido anti-horário (CCW) para fora
    faces = np.array([
        [0, 2, 1], [0, 3, 2], # Face de Baixo
        [4, 5, 6], [4, 6, 7], # Face de Cima
        [0, 1, 5], [0, 5, 4], # Face Frontal
        [2, 3, 7], [2, 7, 6], # Face Traseira
        [0, 4, 7], [0, 7, 3], # Face Esquerda
        [1, 2, 6], [1, 6, 5]  # Face Direita
    ], dtype=int)

    return Mesh(vertices, faces, color)