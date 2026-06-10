import pygame

class Renderer:
    # responsável por conectar as arestas, formando o cubo. 

    def __init__(self, screen): # recebe a tela
        self.screen = screen

    def draw_wireframe(self, projected_vertices, edges):
        if projected_vertices:
            for start, end in edges:

                pygame.draw.line(
                    self.screen,
                    (255,255,255),
                    projected_vertices[start],
                    projected_vertices[end],
                    2
                )

    def draw_point( self, point, color=(255,255,255), radius=5 ):

        x = int(point[0])
        y = int(point[1])

        pygame.draw.circle(
            self.screen,
            color,
            (x,y),
            radius
        )

    def draw_faces(self, projected_vertices, faces):
        for face in faces:
            points = []
            for i in face.vertices:

                if projected_vertices[i] is None:
                    break
                points.append(projected_vertices[i])
            if len(points) != 3:
                continue

            pygame.draw.polygon(
                self.screen,
                face.color,
                points
            )