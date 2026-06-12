import pygame
import numpy as np


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

            pygame.draw.line(
                self.screen,
                colors[i-1],
                (ox, oy),
                (x, y),
                2
            )
            font = pygame.font.SysFont(None, 24)

            labels = ["X", "Y", "Z"]

            text = font.render(
                labels[i-1],
                True,
                colors[i-1]
            )

            self.screen.blit(
                text,
                (x + 5, y + 5)
            )

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