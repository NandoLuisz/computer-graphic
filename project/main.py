import copy
import pygame
import numpy as np
import math

from Io.loader import build_edges, load_mesh
from Io.loader_obj import load_obj


from geometry.vertex_normals import compute_vertex_normals
from geometry.vertex_normals_surface import compute_vertex_normals as compute_vertex_normals_surface

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
    pitch= math.radians(45),
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
    position=np.array([0,0,0]),
    rotation=np.array([0,0,0]),
    scale=np.array([1.0,1.0,1.0])
)

# criando objetos


vertice_pawn, face_pawn = load_obj("models/pinoS.obj")

pawn= Mesh(
    vertices= vertice_pawn,
    edges= build_edges(face_pawn),
    faces= face_pawn,
    vertex_normals= compute_vertex_normals(vertice_pawn, face_pawn),
    position=np.array([4,0,4]),
    rotation=np.array([0,0,0]),
    scale=np.array([2.0, 2.0, 2.0])
)

vertice_queen, face_queen = load_obj("models/rainhaS.obj")

queen= Mesh(
    vertices= vertice_queen,
    edges= build_edges(face_queen),
    faces= face_queen,
    vertex_normals= compute_vertex_normals(vertice_queen, face_queen),
    position=np.array([-4,0,4]),
    rotation=np.array([0,0,0]),
    scale=np.array([2.0, 2.0, 2.0])
)

vertice_king, face_king = load_obj("models/reiS.obj")

king= Mesh(
    vertices= vertice_king,
    edges= build_edges(face_king),
    faces= face_king,
    vertex_normals= compute_vertex_normals(vertice_king, face_king),
    position=np.array([4,0,-4]),
    rotation=np.array([0,0,0]),
    scale=np.array([2.0, 2.0, 2.0])
)

vertice_tower, face_tower = load_obj("models/torre.obj")

tower = Mesh(
    vertices= vertice_tower,
    edges= build_edges(face_tower),
    faces= face_tower,
    vertex_normals= compute_vertex_normals(vertice_tower, face_tower),
    position=np.array([-4,0,-4]),
    rotation=np.array([0,0,0]),
    scale=np.array([2.0, 2.0, 2.0])
)

vertice_lady, face_lady = load_obj("models/damaS.obj")

lady = Mesh(
    vertices= vertice_lady,
    edges= build_edges(face_lady),
    faces= face_lady,
    vertex_normals= compute_vertex_normals(vertice_lady, face_lady),
    position=np.array([0,0,0]),
    rotation=np.array([0,0,0]),
    scale=np.array([2.0, 2.0, 2.0])
)

vertice_surface, face_surface = load_obj("models/tabuleiroBenzier.obj")

surface = Mesh(
    vertices= vertice_surface,
    edges= build_edges(face_surface),
    faces= face_surface,
    vertex_normals= compute_vertex_normals_surface(vertice_surface, face_surface),
    position=np.array([0,-4,0]),
    rotation=np.array([0,0,0]),
    scale=np.array([2.0, 2.0, 2.0])
)



scene.add_mesh(pawn)
scene.add_mesh(queen)
scene.add_mesh(king)
scene.add_mesh(tower)
scene.add_mesh(ground)
scene.add_mesh(lady)

'''scene.add_mesh(surface)'''

'''
scene.add_mesh(queen)'''


scene.camera = camera

# ajustar cores dos solidos

for face in queen.faces:
    face.color = (255, 255, 0)
    
for face in pawn.faces:
    face.color = (0,0,255)
for face in king.faces:
    face.color = (0, 255, 149)
for face in tower.faces:
    face.color = (255, 98, 0)
for face in lady.faces:
    face.color = (162, 0, 255)

light = Light(
    position=np.array([0, 8, 0], dtype=float)
)

scene.add_light(light)
USE_LIGHTING = True
RENDER_MODE = "SOLID" # SOLID, POINT, POLYGON, AUTO

pygame.init()
WIDTH = 800 # largaura de telaa
HEIGHT = 600 # altura da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # criação da tela
clock = pygame.time.Clock() # atualização da tela 
renderer = Renderer (screen) # apontado para a tela para desenhar o objeto
rasterizer = Rasterizer(screen)

render_system = RenderSystem(
    rasterizer,
    renderer,
    WIDTH,
    HEIGHT
)

running = True
while running:
    dt= clock.tick(60) # atualizar acada 60s

    fps = clock.get_fps()
    pygame.display.set_caption(
        f"FPS: {fps:.1f} | Lighting: {USE_LIGHTING} | render_mode: {RENDER_MODE}"
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
    if keys[pygame.K_h]:
        RENDER_MODE = 'SOLID'

    if keys[pygame.K_j]:
        RENDER_MODE = 'POLYGON'
    
    if keys[pygame.K_k]:
        RENDER_MODE = 'POINT'
    
    if keys[pygame.K_l]:
        RENDER_MODE = 'AUTO'

    if keys[pygame.K_n]:
        RENDER_MODE = 'N'

    if keys[pygame.K_TAB]:
        USE_LIGHTING = not USE_LIGHTING
    

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
    render_system.render(scene, USE_LIGHTING, RENDER_MODE)

    # eixo auxiliar

    axes_world = renderer.world_axes(4.0)

    axes_camera, _ = World_to_camera(
        axes_world,
        scene.camera
    )

    axes_projected = perspective(
        axes_camera,
        WIDTH,
        HEIGHT
    )
    light_projected = perspective(
        np.array([light_camera]),
        WIDTH,
        HEIGHT
    )
    renderer.draw_axes(axes_projected)
    if USE_LIGHTING:
        renderer.draw_point(light_projected, 8, (224, 190, 94))
    pygame.display.flip() #redesenha
    '''print(camera.position)'''

pygame.quit()

   

