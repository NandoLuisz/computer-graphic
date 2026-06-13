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
from Box import Box

rei = Mesh()
SEG = 16

# BASE PADRÃO UNIFICADA
circle1 = Circle(radius=0.9, segments=SEG)
base_layer1 = Cylinder(radius=0.9, height=0.2, segments=SEG)
base_layer1.translate(0, 0.1, 0)
base_layer2 = Frustum(bottom_radius=0.9, top_radius=0.7, height=0.2, segments=SEG)
base_layer2.translate(0, 0.3, 0)
base_layer3 = Cylinder(radius=0.7, height=0.15, segments=SEG)
base_layer3.translate(0, 0.475, 0)

rei.merge(circle1)
rei.merge(base_layer1)
rei.merge(base_layer2)
rei.merge(base_layer3)

# CORPO DO REI
corpo = Frustum(bottom_radius=0.68, top_radius=0.40, height=2.2, segments=SEG)
corpo.translate(0, 1.6, 0)
rei.merge(corpo)

# COLARINHO
colarinho = Cylinder(radius=0.52, height=0.15, segments=SEG)
colarinho.translate(0, 2.755, 0)
rei.merge(colarinho)

# COROA DO REI
coroa_rei = Frustum(bottom_radius=0.40, top_radius=0.55, height=0.6, segments=SEG)
coroa_rei.translate(0, 3.11, 0)
rei.merge(coroa_rei)

# ==========================================
# NOVO: TAMPA DA COROA (Para fechar o buraco)
# ==========================================
tampa_rei = Cylinder(radius=0.55, height=0.05, segments=SEG)
tampa_rei.translate(0, 3.41, 0) # Exatamente no topo da coroa
rei.merge(tampa_rei)

# CRUZ SUPERIOR (Ancorada com segurança na tampa)
cruz_v = Box(width=0.12, height=0.45, depth=0.12)
cruz_v.translate(0, 3.60, 0) # Desceu um pouco

cruz_h = Box(width=0.40, height=0.12, depth=0.12)
cruz_h.translate(0, 3.68, 0) # Desceu proporcionalmente

rei.merge(cruz_v)
rei.merge(cruz_h)

if __name__ == "__main__":
    renderer = Renderer3D()
    renderer.render_faces(rei)
    rei.export_obj("Contrução das Peças/listaVerticesFaces/reiS.obj")