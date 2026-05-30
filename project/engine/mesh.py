from dataclasses import dataclass
from engine.face import Face
import numpy as np

@dataclass
class Mesh:
    vertices: np.ndarray

    edges: list
    faces: list[Face]

    position: np.ndarray
    rotation: np.ndarray

    scale: float = 1.0