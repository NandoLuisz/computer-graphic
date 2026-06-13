import sys
import os

pasta_principal = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if pasta_principal not in sys.path: sys.path.append(pasta_principal)
if os.path.join(pasta_principal, 'objects') not in sys.path: sys.path.append(os.path.join(pasta_principal, 'objects'))

from Renderer3D import Renderer3D
from Cylinder import Cylinder
from Tube import Tube
from Mesh import Mesh

dama = Mesh()
SEG = 16

# Reduzido de raio 2.0 para 0.9 para casar perfeitamente na escala do tabuleiro de xadrez
base_dama = Cylinder(radius=0.9, height=0.3, segments=SEG)
base_dama.translate(0, 0.15, 0)
dama.merge(base_dama)

# Ranhuras clássicas concêntricas no topo da pedra usando Tubes planos superpostos
anel1 = Tube(outer_radius=0.8, inner_radius=0.6, height=0.1, segments=SEG)
anel1.translate(0, 0.33, 0)

anel2 = Tube(outer_radius=0.5, inner_radius=0.3, height=0.1, segments=SEG)
anel2.translate(0, 0.33, 0)

centro = Cylinder(radius=0.2, height=0.1, segments=SEG)
centro.translate(0, 0.33, 0)

dama.merge(anel1)
dama.merge(anel2)
dama.merge(centro)

if __name__ == "__main__":
    renderer = Renderer3D()
    renderer.render_faces(dama)
    dama.export_obj("Contrução das Peças/listaVerticesFaces/damaS.obj")