import numpy as np
from engine.face import Face


vertices = np.array([
    [-1,-1,-1],
    [ 1,-1,-1],
    [ 1, 1,-1],
    [-1, 1,-1],
    
    [-1,-1, 1],
    [ 1,-1, 1],
    [ 1, 1, 1],
    [-1, 1, 1]
], dtype=float)

edges = [
    (0,1),
    (1,2),
    (2,3),
    (3,0),

    (4,5),
    (5,6),
    (6,7),
    (7,4),

    (0,4),
    (1,5),
    (2,6),
    (3,7)
]

faces= [
    # frente
    Face(
        vertices=(0,1,2), # vermelho
        color = (255,0,0)
    ),
    Face(
        vertices=(0,2,3), # vermelho
        color = (255,0,0)
    ),

    # trás
    Face(
        vertices=(4,6,5), # verde
        color = (0, 255, 0)
    ),
    Face(
        vertices=(4,7,6), # verde
        color = (0, 255, 0)
    ), 

    # esquerda
    Face(
        vertices=(0,3,7), # azul
        color = (0,0, 255)
    ),
    Face(
        vertices=(0,7,4), # azul
        color = (0,0, 255)
    ),

    #direita
    Face(
        vertices=(1,6,2), # amarelo
        color = (255, 255, 0)
    ),
    Face(
        vertices=(1,5,6), # amarelo
        color = (255, 255, 0)
    ),

    #topo
    Face(
        vertices=(3,2,6), # ciano
        color = (0, 255, 255)
    ),
    Face(
        vertices=(3,6,7), # ciano
        color = (0, 255, 255)
    ),

    #baixo
    Face(
        vertices=(0,5,1), # cinza
        color = (171, 168, 162)
    ),
    Face(
        vertices=(0,4,5), # cinza
        color = (171, 168, 162)
    )
]