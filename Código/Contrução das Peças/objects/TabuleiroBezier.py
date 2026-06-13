import sys
import os

sys.path.append(os.getcwd())

from Vec3 import Vec3
from Mesh import Mesh
from Renderer3D import Renderer3D

def blending_bezier(t):
    u = 1.0 - t
    return [
        u**3,               # B0
        3 * (u**2) * t,     # B1
        3 * u * (t**2),     # B2
        t**3                # B3
    ]

def calcular_superficie_bezier(u, v, matriz_controle):
    bu = blending_bezier(u)
    bv = blending_bezier(v)
    
    x, y, z = 0.0, 0.0, 0.0
    
    for i in range(4):
        for j in range(4):
            peso = bu[i] * bv[j]
            ponto = matriz_controle[i][j]
            
            x += peso * ponto.x
            y += peso * ponto.y
            z += peso * ponto.z
            
    return Vec3(x, y, z)

def gerar_tabuleiro_bezier_com_volume(matriz_controle, resolucao=8, espessura=1.5):
    """
    Gera o tabuleiro distorcido e extruda-o para cima no eixo Y 
    para criar um volume sólido.
    """
    mesh = Mesh()
    pontos_por_camada = (resolucao + 1) * (resolucao + 1)
    
    # ==========================================
    # 1. GERAR VÉRTICES (BASE E TOPO)
    # ==========================================
    for i in range(resolucao + 1):
        for j in range(resolucao + 1):
            u = i / float(resolucao)
            v = j / float(resolucao)
            
            # Vértice da Base
            ponto_base = calcular_superficie_bezier(u, v, matriz_controle)
            mesh.vertices.append(ponto_base)

    for i in range(resolucao + 1):
        for j in range(resolucao + 1):
            u = i / float(resolucao)
            v = j / float(resolucao)
            
            ponto_base = calcular_superficie_bezier(u, v, matriz_controle)
            # Vértice do Topo (Adicionamos a 'espessura' no eixo Y)
            ponto_topo = Vec3(ponto_base.x, ponto_base.y + espessura, ponto_base.z)
            mesh.vertices.append(ponto_topo)

    # ==========================================
    # 2. GERAR FACES (TOPO E BASE)
    # ==========================================
    for i in range(resolucao):
        for j in range(resolucao):
            # Índices da Base
            b0 = i * (resolucao + 1) + j
            b1 = (i + 1) * (resolucao + 1) + j
            b2 = (i + 1) * (resolucao + 1) + (j + 1)
            b3 = i * (resolucao + 1) + (j + 1)
            
            # Índices do Topo (desfasados pelo total de pontos da base)
            t0 = b0 + pontos_por_camada
            t1 = b1 + pontos_por_camada
            t2 = b2 + pontos_por_camada
            t3 = b3 + pontos_por_camada
            
            # Faces da Base (viradas para baixo)
            mesh.faces.append((b0, b2, b1))
            mesh.faces.append((b0, b3, b2))
            
            # Faces do Topo (viradas para cima)
            mesh.faces.append((t0, t1, t2))
            mesh.faces.append((t0, t2, t3))

    # ==========================================
    # 3. GERAR FACES LATERAIS (COSTURAR AS BORDAS)
    # ==========================================
    # Paredes nas bordas horizontais (i = 0 e i = resolucao)
    for j in range(resolucao):
        # Parede Esquerda
        b0 = 0 * (resolucao + 1) + j
        b1 = 0 * (resolucao + 1) + (j + 1)
        t0 = b0 + pontos_por_camada
        t1 = b1 + pontos_por_camada
        mesh.faces.append((b0, t0, t1))
        mesh.faces.append((b0, t1, b1))

        # Parede Direita
        b0 = resolucao * (resolucao + 1) + j
        b1 = resolucao * (resolucao + 1) + (j + 1)
        t0 = b0 + pontos_por_camada
        t1 = b1 + pontos_por_camada
        mesh.faces.append((b0, b1, t1))
        mesh.faces.append((b0, t1, t0))

    # Paredes nas bordas verticais (j = 0 e j = resolucao)
    for i in range(resolucao):
        # Parede Frontal
        b0 = i * (resolucao + 1) + 0
        b1 = (i + 1) * (resolucao + 1) + 0
        t0 = b0 + pontos_por_camada
        t1 = b1 + pontos_por_camada
        mesh.faces.append((b0, b1, t1))
        mesh.faces.append((b0, t1, t0))

        # Parede Traseira
        b0 = i * (resolucao + 1) + resolucao
        b1 = (i + 1) * (resolucao + 1) + resolucao
        t0 = b0 + pontos_por_camada
        t1 = b1 + pontos_por_camada
        mesh.faces.append((b0, t0, t1))
        mesh.faces.append((b0, t1, b1))
            
    mesh.compute_normals()
    return mesh

# Pontos de Controlo da Superfície de Bézier
pontos_controle_tabuleiro = [
    [Vec3(-4, 0, -4),   Vec3(-1.5, 0, -6.5),  Vec3(1.5, 0, -1.5),  Vec3(4, 0, -4)],
    [Vec3(-6.5, 0, -1.5), Vec3(-1.5, 1.0, -1.5), Vec3(1.5, 1.0, -1.5), Vec3(6.5, 0, -1.5)],
    [Vec3(-1.5, 0, 1.5),  Vec3(-1.5, 1.0, 1.5),  Vec3(1.5, 1.0, 1.5),  Vec3(1.5, 0, 1.5)],
    [Vec3(-4, 0, 4),    Vec3(-1.5, 0, 6.5),   Vec3(1.5, 0, 1.5),   Vec3(4, 0, 4)]
]

# Instanciamos a malha do tabuleiro com espessura de 1.5 para cima!
tabuleiro = gerar_tabuleiro_bezier_com_volume(pontos_controle_tabuleiro, resolucao=8, espessura=1.5)

if __name__ == "__main__":
    print(f"Tabuleiro Bézier com Volume gerado! Vértices: {len(tabuleiro.vertices)} | Faces: {len(tabuleiro.faces)}.")
    
    renderer = Renderer3D()
    renderer.render_faces(tabuleiro)
    tabuleiro.export_obj("Contrução das Peças/listaVerticesFaces/tabuleiroBenzier.obj")