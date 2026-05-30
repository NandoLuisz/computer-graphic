import pygame

class Renderer:
    # responsável por conectar as arestas, formando o cubo. 

    def __init__(self, screen): # recebe a tela
        self.screen = screen

    def draw_wireframe(self, projected_vertices, edges):
        print(projected_vertices)
        if projected_vertices:
            for start, end in edges:

                pygame.draw.line(
                    self.screen,
                    (255,255,255),
                    projected_vertices[start],
                    projected_vertices[end],
                    2
                )
    '''def desenhar_ponto(self, projected_vertice):
        if projected_vertice:
            ponto_x = projected_vertice[0][0]
            ponto_y = projected_vertice[0][1]
            print(ponto_x)
            print(ponto_y)
            pygame.draw.circle(
                self.screen, (255,255,255), (ponto_x, ponto_y), 3,0
            )
    '''