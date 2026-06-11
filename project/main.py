import pygame
import numpy as np
import math

from engine.mesh import Mesh
from engine.renderer import Renderer
from engine.rasterizer import Rasterizer
from engine.transform import rotation, translate
from engine.projection import perspective
from engine.camera import Camera, World_to_camera, update_camera
from engine.back_face_culling import back_face
from engine.loader import load_mesh, build_edges
from engine.lighting import vertex_phong
from models.cube import vertices, edges, faces
from engine.vertex_normals import compute_vertex_normals

# criando camera

camera = Camera(
    position= np.array([0, 0, -2]),

    forward= np.array([0,0,0]),

    up= np.array([0,0,0]),
    right=np.array([0,0,0]),
    target= np.array([0, 0, 0]),

    yaw=0.7,
    pitch= 0.3,
    radius=10 
)

# criando objetos

cube = Mesh(
    vertices= vertices,
    edges= edges,
    faces= faces,
    vertex_normals= compute_vertex_normals(vertices, faces),
    position=np.array([0,0,0]),
    rotation=np.array([0,0,0])
)

vertice_dama, face_dama= load_mesh("dama.csv") # importanto figura
dama = Mesh(
    vertices= vertice_dama,
    edges= build_edges(face_dama),
    faces= face_dama,
    vertex_normals= compute_vertex_normals(vertice_dama, face_dama),
    position=np.array([10,0,0]),
    rotation=np.array([0,0,0])
)

vertice_tower, face_tower = load_mesh("tower.csv")
tower = Mesh(
    vertices= vertice_tower,
    edges= build_edges(face_tower),
    faces= face_tower,
    vertex_normals= compute_vertex_normals(vertice_tower, face_tower),
    position=np.array([0,0,0]),
    rotation=np.array([-20,0,0])
)

vertice_queen, face_queen = load_mesh("queen.csv")
queen = Mesh(
    vertices= vertice_queen,
    edges= build_edges(face_queen),
    faces= face_queen,
    vertex_normals= compute_vertex_normals(vertice_queen, face_queen),
    position=np.array([0,0,0]),
    rotation=np.array([-10,0,0])
)

light_position_world = np.array([5, 2, -2], dtype=float)


pygame.init()
WIDTH = 800 # largaura de telaa
HEIGHT = 600 # altura da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # criação da tela
clock = pygame.time.Clock() # atualização da tela 
renderer = Renderer (screen) # apontado para a tela para desenhar o objeto
rasterizer = Rasterizer(screen)

running = True
while running:
    dt= clock.tick(60) # atualizar acada 60s
    fps = clock.get_fps()
    pygame.display.set_caption(
        f"FPS: {fps:.1f}"
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # aperta o icone de feichar
            running=False

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

    camera.pitch = max( -math.pi/2 + 0.1, min(math.pi/2 - 0.1, camera.pitch))

    # coordenadas do mundo
    transformed = rotation(tower.vertices, tower.rotation) # retorna os vetores dos vertices convertidos
    transformed = translate(transformed, tower.position) # translação
    
    update_camera(camera) # atualizar as coordenas da camera

    light_camera, _ = World_to_camera( np.array([light_position_world]), camera)

    light_camera = light_camera[0]

    # coordenadas da camera
    transformed, camera_rotation = World_to_camera( transformed, camera ) # retorna os vetores em coordenadas da câmera

    vertex_normals_camera = ( tower.vertex_normals @ camera_rotation.T)

    #remocendo os vertices que não são visiveis
    visible_faces = back_face(tower.faces, transformed)


    for face in visible_faces:

        i0, i1, i2 = face.vertices

        c0 = vertex_phong(
            transformed[i0],
            vertex_normals_camera[i0],
            light_camera,
            face.color
        )

        c1 = vertex_phong(
            transformed[i1],
            vertex_normals_camera[i1],
            light_camera,
            face.color
        )

        c2 = vertex_phong(
            transformed[i2],
            vertex_normals_camera[i2],
            light_camera,
            face.color
        )
        face.vertex_colors = [
            c0,
            c1,
            c2
        ]

    #projeção em perspectva
    project = perspective(transformed, WIDTH, HEIGHT)

    screen.fill((20,20,20)) # cor de fundo da tela
    rasterizer.clear_zbuffer()
    rasterizer.draw_faces(project, visible_faces)

    # eixo auxiliar

    axes_world = renderer.world_axes(20.0)

    axes_camera, _ = World_to_camera(
        axes_world,
        camera
    )

    axes_projected = perspective(
        axes_camera,
        WIDTH,
        HEIGHT
    )
    renderer.draw_axes(axes_projected)

    pygame.display.flip() #redesenha

pygame.quit()

    

