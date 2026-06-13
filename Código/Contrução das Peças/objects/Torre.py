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

torre = Mesh()
SEG = 16

# BASE PADRÃO UNIFICADA
circle1 = Circle(radius=0.9, segments=SEG)
base_layer1 = Cylinder(radius=0.9, height=0.2, segments=SEG)
base_layer1.translate(0, 0.1, 0)
base_layer2 = Frustum(bottom_radius=0.9, top_radius=0.7, height=0.2, segments=SEG)
base_layer2.translate(0, 0.3, 0)
base_layer3 = Cylinder(radius=0.7, height=0.15, segments=SEG)
base_layer3.translate(0, 0.475, 0)

torre.merge(circle1)
torre.merge(base_layer1)
torre.merge(base_layer2)
torre.merge(base_layer3)

# ==========================================
# CORPO DA TORRE SÓLIDO
# ==========================================
corpo = Frustum(bottom_radius=0.65, top_radius=0.55, height=1.4, segments=SEG)
corpo.translate(0, 1.2, 0)
torre.merge(corpo)

# Plataforma de transição do topo
plataforma = Cylinder(radius=0.68, height=0.15, segments=SEG)
plataforma.translate(0, 1.955, 0)
torre.merge(plataforma)

# Coroa principal do castelo
topo_castelo = Cylinder(radius=0.65, height=0.4, segments=SEG)
topo_castelo.translate(0, 2.21, 0)
torre.merge(topo_castelo)

# Ameias superiores perfeitamente coladas
box_w, box_h, box_d = 0.25, 0.2, 0.25
y_ameia = 2.49

b1 = Box(width=box_w, height=box_h, depth=box_d)
b1.translate(0.5, y_ameia, 0)
b2 = Box(width=box_w, height=box_h, depth=box_d)
b2.translate(-0.5, y_ameia, 0)
b3 = Box(width=box_w, height=box_h, depth=box_d)
b3.translate(0, y_ameia, 0.5)
b4 = Box(width=box_w, height=box_h, depth=box_d)
b4.translate(0, y_ameia, -0.5)

torre.merge(b1)
torre.merge(b2)
torre.merge(b3)
torre.merge(b4)

if __name__ == "__main__":
    renderer = Renderer3D()
    renderer.render_faces(torre)
    torre.export_obj("Contrução das Peças/listaVerticesFaces/torre.obj")