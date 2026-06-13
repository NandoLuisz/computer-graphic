import sys
import os
import math

# Garante que o Python encontre os objetos na pasta pai
pasta_principal = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if pasta_principal not in sys.path: sys.path.append(pasta_principal)
if os.path.join(pasta_principal, 'objects') not in sys.path: sys.path.append(os.path.join(pasta_principal, 'objects'))

from Renderer3D import Renderer3D
from Mesh import Mesh
from Circle import Circle
from Cylinder import Cylinder
from Frustum import Frustum
from Sphere import Sphere

pino = Mesh()
SEG = 16 # Resolução leve para rodar suave no Matplotlib

# ==========================================
# BASE PADRÃO (Peças sobrepostas pelo centro)
# ==========================================
circle1 = Circle(radius=0.9, segments=SEG)

base_layer1 = Cylinder(radius=0.9, height=0.2, segments=SEG)
base_layer1.translate(0, 0.1, 0) # Centro da peça

base_layer2 = Frustum(bottom_radius=0.9, top_radius=0.7, height=0.3, segments=SEG)
base_layer2.translate(0, 0.3, 0) # Sobrepõe com a base anterior

base_layer3 = Cylinder(radius=0.7, height=0.2, segments=SEG)
base_layer3.translate(0, 0.5, 0) 

pino.merge(circle1)
pino.merge(base_layer1)
pino.merge(base_layer2)
pino.merge(base_layer3)

# ==========================================
# CORPO E CABEÇA
# ==========================================
# Corpo afunilado mais alto para conectar a base até o colarinho
corpo = Frustum(bottom_radius=0.6, top_radius=0.3, height=1.4, segments=SEG)
corpo.translate(0, 1.2, 0) # Parte de baixo entra na base, parte de cima encosta no colarinho
pino.merge(corpo)

# Colarinho exatamente na emenda
colarinho = Cylinder(radius=0.4, height=0.1, segments=SEG)
colarinho.translate(0, 1.9, 0)
pino.merge(colarinho)

# Cabeça do Peão conectada ao colarinho
cabeca = Sphere(radius=0.4, stacks=12, sectors=16)
cabeca.translate(0, 2.2, 0) # Como o raio é 0.4, a base da esfera desce até 1.8, fundindo-se ao colarinho
pino.merge(cabeca)

if __name__ == "__main__":
    renderer = Renderer3D()
    renderer.render_faces(pino)
    pino.export_obj("Contrução das Peças/listaVerticesFaces/pinoS.obj")