import math
import pygame
from dataclasses import dataclass
import numpy
import csv


class Pygame3dEngine:

    def __init__(self):

        pygame.init()

        self.running = True

        # resolução
        self.display = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h
        )

        self.screen = pygame.display.set_mode(
            self.display,
            pygame.FULLSCREEN
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Comic Sans", 18)

        # projeção
        self.focal_length = 85
        self.scale = 500

        # câmera
        self.camera = Camera(
            numpy.array([0., 0., 0.]),
            numpy.array([0., 0., 0.])
        )

        # clipping planes
        self.camera_clipping_planes = [

            # near plane
            ClippingPlane((0, 0, 1), 0.1),

            # left
            ClippingPlane(
                (1 / math.sqrt(2), 0, 1 / math.sqrt(2)),
                0
            ),

            # right
            ClippingPlane(
                (-1 / math.sqrt(2), 0, 1 / math.sqrt(2)),
                0
            ),

            # top
            ClippingPlane(
                (0, 1 / math.sqrt(2), 1 / math.sqrt(2)),
                0
            ),

            # bottom
            ClippingPlane(
                (0, -1 / math.sqrt(2), 1 / math.sqrt(2)),
                0
            ),
        ]

    # ==========================================================
    # MODELOS
    # ==========================================================

    @staticmethod
    def load_model(filename: str):

        with open(filename) as csv_file:

            reader = list(csv.DictReader(csv_file))

            triangles = [
                Triangle(
                    int(row["1"]),
                    int(row["2"]),
                    int(row["3"]),
                    row["color"]
                )
                for row in reader
                if row["color"]
            ]

            vertices = numpy.array([
                [
                    float(row["1"]),
                    float(row["2"]),
                    float(row["3"])
                ]
                for row in reader
                if not row["color"]
            ])

        # objeto à frente da câmera
        return Model(
            vertices,
            triangles,
            numpy.array([0., 0., 80.]),
            numpy.array([0., 0., 0.])
        )

    # ==========================================================
    # INPUT
    # ==========================================================

    def check_for_quit(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

    # ==========================================================
    # COORDENADAS
    # ==========================================================

    def to_screen_coordinates(self, x, y):

        return (
            x + self.display[0] / 2,
            y + self.display[1] / 2
        )

    # ==========================================================
    # PROJEÇÃO
    # ==========================================================

    def project_mesh(self, model):

        # rotação do modelo
        vertices = self.rotate(
            model.vertices,
            model.rotation
        )

        # posição do modelo
        vertices = self.translate(
            vertices,
            model.position
        )

        # transformação da câmera
        vertices = self.translate(
            vertices,
            -self.camera.position
        )

        vertices = self.rotate(
            vertices,
            -self.camera.rotation
        )

        # clipping
        triangles = [

            t for t in model.triangles

            if all(
                [
                    self.clip_triangle(
                        plane,
                        t,
                        vertices
                    )

                    for plane in self.camera_clipping_planes
                ]
            )
        ]

        projected_mesh = []

        for triangle in triangles:

            try:

                # evita divisão por zero
                if (
                    vertices[triangle.a][2] <= 0 or
                    vertices[triangle.b][2] <= 0 or
                    vertices[triangle.c][2] <= 0
                ):
                    continue

                points = []

                for vertex_index in [
                    triangle.a,
                    triangle.b,
                    triangle.c
                ]:

                    vertex = vertices[vertex_index]

                    x = (
                        vertex[0] *
                        self.focal_length
                    ) / vertex[2]

                    y = (
                        vertex[1] *
                        self.focal_length
                    ) / vertex[2]

                    x *= self.scale
                    y *= self.scale

                    points.append(
                        self.to_screen_coordinates(x, y)
                    )

                projected_mesh.append(
                    (
                        points[0],
                        points[1],
                        points[2],
                        triangle.color
                    )
                )

            except ZeroDivisionError:
                pass

        return projected_mesh

    def project_scene(self, scene):

        return [
            self.project_mesh(mesh)
            for mesh in scene
        ]

    # ==========================================================
    # RENDER
    # ==========================================================

    def render_mesh(self, projected_mesh):

        for triangle in projected_mesh:

            pygame.draw.polygon(
                self.screen,
                triangle[-1],
                triangle[:3],
                2
            )

    def render_scene(self, projected_scene):

        for mesh in projected_scene:
            self.render_mesh(mesh)

    # ==========================================================
    # TRANSFORMAÇÕES
    # ==========================================================

    @staticmethod
    def translate(vertices, translation):

        return vertices + translation

    @staticmethod
    def rotate(vertices, rotation):

        rotation = rotation * math.pi / 180

        # rotação Z
        rotation_z_matrix = numpy.array([
            [
                math.cos(rotation[2]),
                -math.sin(rotation[2]),
                0
            ],
            [
                math.sin(rotation[2]),
                math.cos(rotation[2]),
                0
            ],
            [
                0,
                0,
                1
            ],
        ])

        # rotação Y
        rotation_y_matrix = numpy.array([
            [
                math.cos(rotation[1]),
                0,
                math.sin(rotation[1])
            ],
            [
                0,
                1,
                0
            ],
            [
                -math.sin(rotation[1]),
                0,
                math.cos(rotation[1])
            ],
        ])

        # rotação X
        rotation_x_matrix = numpy.array([
            [
                1,
                0,
                0
            ],
            [
                0,
                math.cos(rotation[0]),
                -math.sin(rotation[0])
            ],
            [
                0,
                math.sin(rotation[0]),
                math.cos(rotation[0])
            ],
        ])

        x_rotated = numpy.tensordot(
            rotation_x_matrix,
            vertices,
            axes=(1, 1)
        ).T

        xy_rotated = numpy.tensordot(
            rotation_y_matrix,
            x_rotated,
            axes=(1, 1)
        ).T

        xyz_rotated = numpy.tensordot(
            rotation_z_matrix,
            xy_rotated,
            axes=(1, 1)
        ).T

        return xyz_rotated

    # ==========================================================
    # CLIPPING
    # ==========================================================

    def clip_triangle(self, plane, triangle, vertices):

        distances = numpy.array([
            self.get_signed_distance(
                plane,
                vertices[triangle.a]
            ),

            self.get_signed_distance(
                plane,
                vertices[triangle.b]
            ),

            self.get_signed_distance(
                plane,
                vertices[triangle.c]
            )
        ])

        if all(distances > 0):
            return True

        elif all(distances < 0):
            return False

        else:
            return True

    @staticmethod
    def get_signed_distance(plane, vertex):

        normal_x, normal_y, normal_z = plane.normal

        vertex_x, vertex_y, vertex_z = vertex

        return (
            vertex_x * normal_x +
            vertex_y * normal_y +
            vertex_z * normal_z +
            plane.distance_to_origin
        )

    # ==========================================================
    # FRAME
    # ==========================================================

    def flip(self):

        pygame.display.flip()

        self.screen.fill("black")

        self.clock.tick(60)


# ==============================================================
# DATA CLASSES
# ==============================================================

@dataclass
class Triangle:
    a: int
    b: int
    c: int
    color: str


@dataclass
class Camera:
    position: numpy.ndarray
    rotation: numpy.ndarray


@dataclass
class Model:
    vertices: numpy.ndarray
    triangles: list
    position: numpy.ndarray
    rotation: numpy.ndarray


@dataclass
class ClippingPlane:
    normal: tuple
    distance_to_origin: float


'''
import math 
import pygame
from dataclasses import dataclass
import numpy
import csv

class Pygame3dEngine:
    def __init__ (self):
        pygame.init() #iniciando pygame
        self.running= True
        
        self.focal_length = 85
        self.scale = 500
        self.camera = Camera(numpy.array([0., 0., 0.]), numpy.array([0., 0., 0.]))
        self.camera_clipping_planes = [
            ClippingPlane((0, 0, 1), self.focal_length),
            ClippingPlane((1 / math.sqrt(2), 0, 1 / math.sqrt(2)), 0),
            ClippingPlane((-1 / math.sqrt(2), 0, 1 / math.sqrt(2)), 0),
            ClippingPlane((0, 1 / math.sqrt(2), 1 / math.sqrt(2)), 0),
            ClippingPlane((0, -1 / math.sqrt(2), 1 / math.sqrt(2)), 0),
        ]

        self.display = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.font = pygame.font.SysFont('Comic Sans', 12)
        self.screen = pygame.display.set_mode(self.display, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        

    @staticmethod
    def load_model(filename: str) -> dataclass:
        with open(filename) as csv_file:
            reader = list(csv.DictReader(csv_file))
            triangle = [Triangle(*[int(i) for i in list(row.values())[:3]], row["color"]) for row in reader if row["color"]]
            vertices = numpy.array([[float(i) for i in list(row.values())[:3]] for row in reader if not row["color"]])
        return Model(vertices, triangle, [-2, 0, 0], numpy.array([0, 0, 0]))


    def check_for_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    #cerverte a origem de quaisquer coordenada 2D para o centro da tela
    def to_screen_coordinates(self, x: float, y: float) -> tuple[float, float]:
        return x + self.display[0] / 2, y + self.display[1] / 2

    # pega qualquer coordenada 2D com sua origem no centro da tela e altera a origem para o canto superior esquerdo.
    def to_rotation_coordinates(self, x: float, y: float) -> tuple[float, float]:
        return x - self.display[0] / 2, y - self.display[1] / 2
    
    #função condensada que realizar rotação e translação
    def project_mesh(self, model: dataclass):
        vertices = self.rotate(model.vertices, rotation=model.rotation)
        vertices = self.translate(vertices, translation=model.position)
        vertices = self.translate(vertices, translation=self.camera.position)
        vertices = self.rotate(vertices, rotation=self.camera.rotation)
        triangles = [t for t in model.triangles if all([self.clip_triangle(p, t, vertices) for p in self.camera_clipping_planes])]
        projected_x = [(vertex[0] * self.focal_length) / vertex[-1] for vertex in vertices]
        projected_y = [(vertex[1] * self.focal_length) / vertex[-1] for vertex in vertices]
        return ((self.to_screen_coordinates(projected_x[triangle.a] * self.scale, projected_y[triangle.a] * self.scale),
                 self.to_screen_coordinates(projected_x[triangle.b] * self.scale, projected_y[triangle.b] * self.scale),
                 self.to_screen_coordinates(projected_x[triangle.c] * self.scale, projected_y[triangle.c] * self.scale),
                 triangle.color) for triangle in triangles)
    

    def project_scene(self, scene):
        return [self.project_mesh(mesh) for mesh in scene]

    def render_mesh(self, projected_mesh):
        for triangle in projected_mesh:
            pygame.draw.polygon(self.screen, triangle[-1], triangle[:3], 5)

    def render_scene(self, projected_scene):
        for projected_mesh in projected_scene:
            self.render_mesh(projected_mesh)

    # move qualquer objeto no espaço XYZ usando as matrizes acima
    @staticmethod
    def translate(vertices, translation):
        return vertices + translation
    
    #realiza uma operação de rotação no objeto dado usando todas as três matrizes de rotação acima.
    @staticmethod
    def rotate(vertices, rotation: numpy.ndarray):
        rotation = rotation * math.pi / 180
        rotation_z_matrix = numpy.array([
            [math.cos(rotation[2]), -math.sin(rotation[2]), 0],
            [math.sin(rotation[2]), math.cos(rotation[2]), 0],
            [0, 0, 1],
        ])
        rotation_y_matrix = numpy.array([
            [math.cos(rotation[1]), 0, math.sin(rotation[1])],
            [0, 1, 0],
            [-math.sin(rotation[1]), 0, math.cos(rotation[1])],
        ])
        rotation_x_matrix = numpy.array([
            [1, 0, 0],
            [0, math.cos(rotation[0]), -math.sin(rotation[0])],
            [0, math.sin(rotation[0]), math.cos(rotation[0])],
        ])
        x_rotated = numpy.tensordot(rotation_x_matrix, vertices, axes=(1, 1)).T
        xy_rotated = numpy.tensordot(rotation_y_matrix, x_rotated, axes=(1, 1)).T
        xyz_rotated = numpy.tensordot(rotation_z_matrix, xy_rotated, axes=(1, 1)).T
        return xyz_rotated

    def clip_triangle(self, plane, triangle, vertices):
        distances = numpy.array([
            self.get_signed_distance(plane, vertices[triangle.a]),
            self.get_signed_distance(plane, vertices[triangle.b]),
            self.get_signed_distance(plane, vertices[triangle.c])
        ])

        if all(distances > 0):
            return True
        elif all(distances < 0):
            return False
        else:
            return True

    @staticmethod
    def get_signed_distance(plane, vertex):
        normal_x, normal_y, normal_z = plane.normal
        vertex_x, vertex_y, vertex_z = vertex
        return vertex_x * normal_x + (vertex_y * normal_y) + (vertex_z * normal_z) + plane.distance_to_origin


    def flip(self):
        pygame.display.flip()
        self.screen.fill("black")
        self.clock.tick(60)

@dataclass
class Triangle:
    a: int
    b: int
    c: int
    color: str

@dataclass
class Camera:
    position: numpy.ndarray
    rotation: numpy.ndarray


@dataclass
class Model:
    vertices: numpy.ndarray
    triangles: list
    position: list
    rotation: numpy.ndarray
    
@dataclass
class ClippingPlane:
    normal: tuple
    distance_to_origin: float


'''

