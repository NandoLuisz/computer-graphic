import numpy as np

class Mesh:
    def __init__(self, vertices, faces, color):
        self.vertices = np.array(vertices, dtype=float)
        self.faces = np.array(faces, dtype=int)
        self.color = np.array(color, dtype=float)
        self.normals = []
        self.compute_normals()

    def compute_normals(self):
        normals = []
        for face in self.faces:
            v0 = self.vertices[face[0]][:3]
            v1 = self.vertices[face[1]][:3]
            v2 = self.vertices[face[2]][:3]
            edge1 = v1 - v0
            edge2 = v2 - v0
            n = np.cross(edge1, edge2)
            norm = np.linalg.norm(n)
            if norm > 0: n = n / norm
            normals.append(n)
        self.normals = np.array(normals)

def generate_revolutions_mesh(profile_points, sectors=32, color=[1.0, 1.0, 1.0]):
    vertices = []
    faces = []
    num_profile = len(profile_points)

    # Gerar os vértices rotacionando o contorno em torno de Z
    for i in range(sectors):
        theta = 2.0 * np.pi * i / sectors
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        for (x, z) in profile_points:
            vertices.append([x * cos_t, x * sin_t, z, 1.0])

    # Conectar os vértices criando a malha de triângulos
    for i in range(sectors):
        next_i = (i + 1) % sectors
        for j in range(num_profile - 1):
            p0 = i * num_profile + j
            p1 = i * num_profile + (j + 1)
            p2 = next_i * num_profile + j
            p3 = next_i * num_profile + (j + 1)
            
            # Triangulação CCW (sentido anti-horário)
            faces.append([p0, p2, p1])
            faces.append([p1, p2, p3])

    return Mesh(vertices, faces, color)

def create_checker_piece(color=[0.8, 0.1, 0.1]):
    # Silhueta da peça de dama (X=Raio, Z=Altura)
    profile = [
        (0.0, 0.0),   # Centro da base
        (1.0, 0.0),   # Borda externa inferior
        (1.0, 0.15),  # Lateral inferior
        (0.85, 0.15), # Detalhe para dentro (ranhura)
        (0.85, 0.25), # Sobe a ranhura
        (1.0, 0.25),  # Volta para a borda externa
        (1.0, 0.4),   # Lateral superior
        (0.0, 0.4)    # Centro do topo (fecha a tampa)
    ]
    return generate_revolutions_mesh(profile, sectors=32, color=color)