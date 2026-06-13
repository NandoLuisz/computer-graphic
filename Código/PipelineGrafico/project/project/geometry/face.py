from dataclasses import dataclass
import numpy as np

@dataclass
class Face:

    vertices: tuple[int, int, int]

    color: tuple[int, int, int]

    shaded_color: tuple[int, int, int] | None = None

    vertex_colors: list | None = None

    normal: np.ndarray | None = None

    center: np.ndarray | None = None

    material_id: int = 0

    depth: float = 0.0

    def __post_init__(self):
        self.shaded_color = self.color