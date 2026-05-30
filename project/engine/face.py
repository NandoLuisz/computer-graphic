from dataclasses import dataclass
import numpy as np

@dataclass
class Face:

    vertices: tuple[int, int, int]

    color: tuple[int, int, int]

    normal: np.ndarray | None = None

    material_id: int = 0

    depth: float = 0.0

