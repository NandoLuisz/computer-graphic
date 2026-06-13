import pygame
import numpy as np

from rendering.projection import perspective
from scene.camera import World_to_camera


class Renderer:
    # responsável por conectar as arestas, formando o cubo. 

    def __init__(self, screen): # recebe a tela
        self.screen = screen


    def draw_wireframe(self, projected_vertices, edges):

        for start, end in edges:

            p1 = projected_vertices[start]
            p2 = projected_vertices[end]

            if p1 is None or p2 is None:
                continue

            pygame.draw.line(
                self.screen,
                (255,255,255),
                (p1[0], p1[1]),
                (p2[0], p2[1]),
                1
            )
    

    def draw_point( self, points, radius, color = (255, 0, 0) ):

        for point in points:

            if point is not None:

                x = int(point[0])
                y = int(point[1])

                pygame.draw.circle(
                    self.screen,
                    color,
                    (x, y),
                    radius
                )


    def draw_faces(self, projected_vertices, faces):

        for face in faces:

            points = []

            for i in face.vertices:

                p = projected_vertices[i]

                if p is None:
                    break

                x, y, _ = p

                points.append((x, y))

            if len(points) != 3:
                continue

            pygame.draw.polygon(
                self.screen,
                face.color,
                points
            )


    
    def draw_triangle_edges(self, projected_vertices, faces):

        for face in faces:

            points = []

            for i in face.vertices:

                if projected_vertices[i] is None:
                    break

                points.append(
                    (
                        projected_vertices[i][0],
                        projected_vertices[i][1]
                    )
                )

            if len(points) != 3:
                continue

            pygame.draw.polygon(
                self.screen,
                (255,255,255),
                points,
                1
            )

    def draw_stats(self, stats):

        font = pygame.font.SysFont(None, 15)

        y = 10

        for text in stats:

            surface = font.render(
                text,
                True,
                (255,255,255)
            )

            self.screen.blit(surface, (10, y))

            y += 25

    
    def draw_axes(self, projected):

        origin = projected[0]

        if origin is None:
            return

        ox, oy, _ = origin

        pygame.draw.circle(
            self.screen,
            (255,255,255),
            (int(ox), int(oy)),
            4
        )

        colors = [
            (179, 30, 30),  # X
            (28, 110, 8),  # Y
            (5, 19, 150)   # Z
        ]

        for i in range(1,4):

            if projected[i] is None:
                continue

            x, y, _ = projected[i]

            pygame.draw.line( self.screen, colors[i-1], (ox, oy), (x, y), 2)
            font = pygame.font.SysFont(None, 24)

            labels = ["X", "Y", "Z"]

            text = font.render( labels[i-1], True, colors[i-1])

            self.screen.blit( text, (x + 5, y + 5))

    def world_axes(self, size):

        return np.array([
            [0, 0, 0],      # origem

            [size, 0, 0],   # X
            [0, size, 0],   # Y
            [0, 0, size]    # Z
        ], dtype=float)
    
    def world_grid(self, size=10, step=1):

        lines = []

        for i in range(-size, size + 1, step):

            lines.append([
                [-size, 0, i],
                [ size, 0, i]
            ])

            lines.append([
                [i, 0, -size],
                [i, 0,  size]
            ])

        return lines

    def draw_camera_axes(self, camera, x=730, y=530, size=50):

        origin = (int(x), int(y))

        axes = [
            (camera.right,   (255, 0, 0), "X"),
            (camera.up,      (0, 255, 0), "Y"),
            (camera.forward, (0, 0, 255), "Z")
        ]

        font = pygame.font.SysFont(None, 24)

        for direction, color, label in axes:

            end_x = int(x + direction[0] * size)
            end_y = int(y - direction[1] * size)

            pygame.draw.line(
                self.screen,
                color,
                origin,
                (end_x, end_y),
                3
            )

            text = font.render(
                label,
                True,
                color
            )

            self.screen.blit(
                text,
                (end_x + 5, end_y + 5)
            )
            pygame.draw.circle(
                self.screen,
                (255,255,255),
                origin,
                4
            )

            pygame.draw.circle(
                self.screen,
                (255,255,255),
                (800//2, 600//2),
                5
            )

    def render_grid( self, camera, width, height, size=20, step=1):

        lines = self.world_grid(size, step)

        for line in lines:

            vertices = np.array(line)

            camera_vertices, _ = World_to_camera(
                vertices,
                camera
            )

            projected = perspective(
                camera_vertices,
                width,
                height
            )

            if projected[0] is None or projected[1] is None:
                continue

            pygame.draw.line(
                self.screen,
                (70,70,70),
                (projected[0][0], projected[0][1]),
                (projected[1][0], projected[1][1]),
                1
            )