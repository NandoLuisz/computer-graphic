from dataclasses import dataclass, field
import numpy as np

class Scene:

    def __init__(self):

        self.meshes = []

        self.lights = []

        self.camera = None

    def add_mesh(self, mesh):

        self.meshes.append(mesh)

    def add_light(self, light):

        self.lights.append(light)

    def set_camera(self, camera):

        self.camera = camera