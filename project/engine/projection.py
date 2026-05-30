import numpy as np

#responsável por fazer a projeção em perspectiva
# devolve um conjunto de vertices convertidos para o sistema de coordenadas de projeção (3D->2D)
# x'=x.f/z
# y'=y.f/z
#fov = é adistancia da câmera e o plano de projeção 
#vertices no scc



def perspective(vertices, width, height, focal_length=200):

    projected = []

    NEAR = 0.1

    for x, y, z in vertices:

        if z <= NEAR:
            z = NEAR

        px = (x * focal_length) / z
        py = (y * focal_length) / z

        screen_x = int(px + width / 2)
        screen_y = int(-py + height / 2)
        
        projected.append((screen_x, screen_y))
        print(projected)
    return projected