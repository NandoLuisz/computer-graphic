import pygame
import numpy as np
import math

from engine.mesh import Mesh
from engine.renderer import Renderer
from engine.transform import rotation, translate
from engine.projection import perspective
from engine.camera import Camera, World_to_camera, update_camera

from models.cube import vertices, edges, faces
from models.figura1 import vertices as v, edges as a
from models.ponto import ponto , edge as e

pygame.init()

WIDTH = 800 # largaura de telaa
HEIGHT = 600 # altura da tela

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # criação da tela
clock = pygame.time.Clock() # atualização da tela 


renderer = Renderer (screen) # apontado para a tela para desenhar o objeto
camera = Camera(
    position= np.array([0, 0, 0]),

    forward= np.array([0,0,0]),

    up= np.array([0,0,0]),
    right=np.array([0,0,0]),
    target= np.array([0, 0, 3]),

    yaw=0.7,
    pitch= 0.3,
    radius=10 
)



cube = Mesh(
    vertices= vertices,
    edges= edges,
    faces= faces,
    position=np.array([0,0,0]),
    rotation=np.array([0,0,0])
)



'''figura = Mesh(
    vertices= v,
    edges= a,
    position = np.array([0,10,20]),
    rotation=np.array([0,0,0])
)
'''
running = True
while running:
    dt= clock.tick(60) # atualizar acada 60s
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # aperta o icone de feichar
            running=False
    #cube.rotation[0] +=1 # rotação em x
    #cube.rotation[1] +=1 #rotação em y

    # rotação horizaontal -> yaw rotaciona entorno do eixo Y 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera.yaw -=0.02
    if keys[pygame.K_RIGHT]:
        camera.yaw += 0.02

    #rotação vertical
    if keys[pygame.K_UP]:
        camera.pitch += 0.02

    if keys[pygame.K_DOWN]:
        camera.pitch -= 0.02

    #zoom
    if keys[pygame.K_q]:
        camera.radius += 0.2

    if keys[pygame.K_e]:
        camera.radius -= 0.2

    camera.pitch = max(
        -math.pi/2 + 0.1,
        min(math.pi/2 - 0.1, camera.pitch)
    
    )

    # coordenadas do mundo
    transformed = rotation(cube.vertices, cube.rotation) # retorna os vetores dos vertices convertidos
    transformed = translate(transformed, cube.position) # translação
    # atualizar as coordenas da camera:
    update_camera(camera)

    # coordenadas da camera
    transformed = World_to_camera(transformed, camera) # retorna os vetores em coordenadas da câmera

    #projeção em perspectva
    project = perspective(transformed, WIDTH, HEIGHT)

    screen.fill((20,20,20)) # cor de fundo da tela
    
    #desenhando o objeto
    renderer.draw_faces(project, cube.faces)
    #renderer.draw_wireframe(project, cube.edges)
    #renderer.desenhar_ponto(project)


    pygame.display.flip() #redesenha

pygame.quit()

    

