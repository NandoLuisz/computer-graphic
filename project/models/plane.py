import numpy as np
from geometry.face import Face

vertices = np.array([
    [-5, 0, -5],  # 0
    [ 5, 0, -5],  # 1
    [ 5, 0,  5],  # 2
    [-5, 0,  5]   # 3
], dtype=float)

edges = [
    (0,1),
    (1,2),
    (2,3),
    (3,0)
]

faces = [
    Face((0,1,2), (80,120,80)),
    Face((0,2,3), (80,120,80))
]