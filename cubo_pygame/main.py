import time
import pygame
from pygame3dengine import Pygame3dEngine


import os

BASE_DIR = os.path.dirname(__file__)

csv_path = os.path.join(BASE_DIR, "cube.csv")


engine = Pygame3dEngine()
pygame.mouse.set_visible(False)
model = engine.load_model(csv_path)
scene = [model]

while engine.running:

    engine.check_for_quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
        engine.running = False

    # =====================================
    # ROTAÇÃO COM MOUSE
    # =====================================

    if pygame.mouse.get_pressed()[0]:

        mouse_dx, mouse_dy = pygame.mouse.get_rel()

        # eixo Y -> movimento horizontal
        scene[0].rotation[1] += mouse_dx * 0.5

        # eixo X -> movimento vertical
        scene[0].rotation[0] += mouse_dy * 0.5

    else:

        # evita salto quando clicar novamente
        pygame.mouse.get_rel()

    # =====================================
    # RENDER
    # =====================================

    projected_mesh = engine.project_scene(scene)

    engine.render_scene(projected_mesh)

    engine.flip()

pygame.quit()


'''
import time
import pygame

from pygame3dengine import Pygame3dEngine

engine = Pygame3dEngine()
pygame.mouse.set_visible(False)
model = engine.load_model("cube.csv")
scene = [model]

while engine.running:
    engine.check_for_quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
        engine.running = False

    start = time.time()
    projected_mesh = engine.project_scene(scene)
    end = time.time()
    project_latency = end - start

    start = time.time()
    engine.render_scene(projected_mesh)
    end = time.time()
    render_latency = end - start

    scene[0].rotation += 1

    text_surface = engine.font.render(f"Rotation: {engine.camera.rotation} | Position: {engine.camera.position} | {project_latency} | {render_latency}", True, (255, 255, 255))
    engine.screen.blit(text_surface, (0, 0))
    engine.flip()

pygame.quit()
'''