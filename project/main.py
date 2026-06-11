import copy
import pygame
import numpy as np
import math

from Io.loader import build_edges, load_mesh
from Io.loader_obj import load_obj

from geometry.vertex_normals import compute_vertex_normals

from rendering.projection import perspective
from rendering.rasterizer import Rasterizer
from rendering.render_system import RenderSystem
from rendering.renderer import Renderer

from scene.camera import Camera, World_to_camera, update_camera
from scene.light import Light
from scene.mesh import Mesh
from scene.scene import Scene

from models.cube import vertices, edges, faces
from models.plane import ( vertices as plane_vertices, edges as plane_edges, faces as plane_faces)


scene = Scene()

# criando camera

camera = Camera(
    position= np.array([0, 0, -2]),

    forward= np.array([0,0,0]),

    up= np.array([0,0,0]),
    right=np.array([0,0,0]),
    target= np.array([0, 0, 0]),

    yaw=math.radians(45),
    pitch= math.radians(25),
    radius=20 
)

scene.set_camera(camera)

#criando plano
plane_normals = np.array([
    [0,1,0],
    [0,1,0],
    [0,1,0],
    [0,1,0]
], dtype=float)

ground = Mesh(
    vertices=plane_vertices.copy(),
    edges=plane_edges,
    faces=copy.deepcopy(plane_faces),
    vertex_normals=plane_normals,
    position=np.array([0,-2,0]),
    rotation=np.array([0,0,0]),
    scale=np.array([1.0,1.0,1.0])
)

# criando objetos

cube1 = Mesh(
    vertices=vertices.copy(),
    edges=edges,
    faces=copy.deepcopy(faces),
    vertex_normals=compute_vertex_normals(vertices, faces),
    position=np.array([-3,0,-3]),
    rotation=np.array([0,0,0]),
    scale=np.array([1.0, 1.0, 1.0])
)

cube2 = Mesh(
    vertices=vertices.copy(),
    edges=edges,
    faces=copy.deepcopy(faces),
    vertex_normals=compute_vertex_normals(vertices, faces),
    position=np.array([3,0,-3]),
    rotation=np.array([0,0,0]),
    scale=np.array([1.0, 1.0, 1.0])
)

cube3 = Mesh(
    vertices=vertices.copy(),
    edges=edges,
    faces=copy.deepcopy(faces),
    vertex_normals=compute_vertex_normals(vertices, faces),
    position=np.array([-3,0,3]),
    rotation=np.array([0,0,0]),
    scale=np.array([1.0, 1.0, 1.0])
)

cube4 = Mesh(
    vertices=vertices.copy(),
    edges=edges,
    faces=copy.deepcopy(faces),
    vertex_normals=compute_vertex_normals(vertices, faces),
    position=np.array([3,0,3]),
    rotation=np.array([0,0,0]),
    scale=np.array([1.0, 1.0, 1.0])
)



vertice_dama, face_dama= load_mesh("models/dama.csv") # importanto figura
dama = Mesh(
    vertices= vertice_dama,
    edges= build_edges(face_dama),
    faces= face_dama,
    vertex_normals= compute_vertex_normals(vertice_dama, face_dama),
    position=np.array([10,0,0]),
    rotation=np.array([0,0,0]), 
    scale=np.array([1.0, 1.0, 1.0])
)

vertice_tower, face_tower = load_mesh("models/tower.csv")
tower = Mesh(
    vertices= vertice_tower,
    edges= build_edges(face_tower),
    faces= face_tower,
    vertex_normals= compute_vertex_normals(vertice_tower, face_tower),
    position=np.array([0,0,0]),
    rotation=np.array([-20,0,0]), 
    scale=np.array([1.0, 1.0, 1.0])
)

vertice_queen, face_queen = load_mesh("models/queen.csv")
queen = Mesh(
    vertices= vertice_queen,
    edges= build_edges(face_queen),
    faces= face_queen,
    vertex_normals= compute_vertex_normals(vertice_queen, face_queen),
    position=np.array([0,0,0]),
    rotation=np.array([-10,0,0]),
    scale=np.array([1.0, 1.0, 1.0])
)

vertice_pino, face_pino = load_obj("models/pinoS.obj")

pino= Mesh(
    vertices= vertice_pino,
    edges= build_edges(face_pino),
    faces= face_pino,
    vertex_normals= compute_vertex_normals(vertice_pino, face_pino),
    position=np.array([0,0,0]),
    rotation=np.array([-10,0,0]),
    scale=np.array([4.0, 4.0, 4.0])
)

'''scene.add_mesh(cube1)
scene.add_mesh(cube2)
scene.add_mesh(cube3)
scene.add_mesh(cube4)
scene.add_mesh(ground)
'''
scene.add_mesh(pino)


scene.camera = camera

# ajustar cores dos solidos

for face in cube1.faces:
    face.color = (255,0,0)

for face in cube2.faces:
    face.color = (0,255,0)

for face in cube3.faces:
    face.color = (0,0,255)

for face in cube4.faces:
    face.color = (255,255,0)
for face in ground.faces:
    face.color = (80, 120, 80)

light = Light(
    position=np.array([5, 2, -2], dtype=float)
)

scene.add_light(light)

pygame.init()
WIDTH = 800 # largaura de telaa
HEIGHT = 600 # altura da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # criação da tela
clock = pygame.time.Clock() # atualização da tela 
renderer = Renderer (screen) # apontado para a tela para desenhar o objeto
rasterizer = Rasterizer(screen)

render_system = RenderSystem(
    rasterizer,
    WIDTH,
    HEIGHT
)

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
        scene.camera.yaw -= 0.02

    if keys[pygame.K_RIGHT]:
        scene.camera.yaw += 0.02

    if keys[pygame.K_UP]:
        scene.camera.pitch += 0.02

    if keys[pygame.K_DOWN]:
        scene.camera.pitch -= 0.02

    if keys[pygame.K_q]:
        scene.camera.radius += 0.2

    if keys[pygame.K_e]:
        scene.camera.radius -= 0.2

    scene.camera.pitch = max( -math.pi/2 + 0.1, min(math.pi/2 - 0.1, camera.pitch))

    update_camera(scene.camera) # atualizar as coordenas da camera


    light = scene.lights[0]

    light_camera, _ = World_to_camera(
        np.array([light.position]),
        scene.camera
    )
    light_camera = light_camera[0]

    screen.fill((20,20,20)) # cor de fundo da tela

    rasterizer.clear_zbuffer()
    render_system.render(scene)

    # eixo auxiliar

    axes_world = renderer.world_axes(5.0)

    axes_camera, _ = World_to_camera(
        axes_world,
        scene.camera
    )

    axes_projected = perspective(
        axes_camera,
        WIDTH,
        HEIGHT
    )
    renderer.draw_axes(axes_projected)

    pygame.display.flip() #redesenha

pygame.quit()

    

