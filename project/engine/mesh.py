from dataclasses import dataclass
import numpy as np

@dataclass
class Mesh:
    vertices: np.ndarray
    edges: list

    position: np.ndarray
    rotation: np.ndarray

    scale: float = 0.5
