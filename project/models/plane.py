import numpy as np
from geometry.face import Face

vertices = np.array([
    [-6, 0, -6],  # 0
    [ 6, 0, -6],  # 1
    [ 6, 0,  6],  # 2
    [-6, 0,  6]   # 3
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