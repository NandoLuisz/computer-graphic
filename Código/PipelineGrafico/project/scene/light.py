from dataclasses import dataclass
import numpy as np

@dataclass
class Light:

    position: np.ndarray

    color: tuple = (255,255,255)

    intensity: float = 1.0