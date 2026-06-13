import sys
import os
import math

pasta_principal = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if pasta_principal not in sys.path: sys.path.append(pasta_principal)
if os.path.join(pasta_principal, 'objects') not in sys.path: sys.path.append(os.path.join(pasta_principal, 'objects'))

from Renderer3D import Renderer3D
from Mesh import Mesh
from Circle import Circle
from Cylinder import Cylinder
from Frustum import Frustum
from Sphere import Sphere

rainha = Mesh()
SEG = 16

# BASE PADRÃO UNIFICADA
circle1 = Circle(radius=0.9, segments=SEG)
base_layer1 = Cylinder(radius=0.9, height=0.2, segments=SEG)
base_layer1.translate(0, 0.1, 0)
base_layer2 = Frustum(bottom_radius=0.9, top_radius=0.7, height=0.2, segments=SEG)
base_layer2.translate(0, 0.3, 0)
base_layer3 = Cylinder(radius=0.7, height=0.15, segments=SEG)
base_layer3.translate(0, 0.475, 0)

rainha.merge(circle1)
rainha.merge(base_layer1)
rainha.merge(base_layer2)
rainha.merge(base_layer3)

# CORPO ALTO E COMPACTADO
corpo = Frustum(bottom_radius=0.65, top_radius=0.35, height=2.2, segments=SEG)
corpo.translate(0, 1.6, 0)
rainha.merge(corpo)

# COLARINHO
colarinho = Cylinder(radius=0.45, height=0.15, segments=SEG)
colarinho.translate(0, 2.755, 0)
rainha.merge(colarinho)

# COROA INVERTIDA (Agora com a base fechada)
coroa = Frustum(bottom_radius=0.35, top_radius=0.60, height=0.5, segments=SEG)
coroa.translate(0, 3.06, 0)
rainha.merge(coroa)

# ==========================================
# NOVO: TAMPA DA COROA (Para fechar o buraco)
# ==========================================
tampa_coroa = Cylinder(radius=0.60, height=0.05, segments=SEG)
tampa_coroa.translate(0, 3.31, 0) # Posicionada exatamente no topo do Frustum
rainha.merge(tampa_coroa)

# MINI ESFERA DO TOPO (Apoiada e levemente afundada na tampa)
topo_esfera = Sphere(radius=0.15, stacks=8, sectors=16)
topo_esfera.translate(0, 3.42, 0) 
rainha.merge(topo_esfera)

if __name__ == "__main__":
    renderer = Renderer3D()
    renderer.render_faces(rainha)
    rainha.export_obj("Contrução das Peças/listaVerticesFaces/rainhaS.obj")