from dataclasses import dataclass
from geometry.face import Face
import numpy as np

@dataclass
class Mesh:
    vertices: np.ndarray

    edges: list
    faces: list[Face]
    vertex_normals: np.ndarray 
    
    position: np.ndarray
    rotation: np.ndarray

    scale:np.ndarray