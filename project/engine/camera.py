from dataclasses import dataclass
import numpy as np
import math

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def World_to_camera(vertices, camera):
    # normalização de vetores, utlizando o metodo do professor
    relative = camera.target - camera.position
    camera.forward = normalize(relative) # encontrado o vetor que aponta para frente
    #criação de um vetor auxiliar chmado world_up para encontrar os outros vetores da camera.
    #caso o ponto onde a cara está apontado forma um vetor paraleo com o vetor auxiliar,
    #nesse caso, o vetor, em vez de apontar para cima, apontará para o lado
    if abs(camera.forward[1])>0.99:
        world_up = np.array([1,0,0], dtype=float) # aponta para o lado, caso o vetor forward já estiver apontando para cima
    else:
        world_up = np.array([0,1,0], dtype=float)

    camera.right = np.cross(camera.forward, world_up)
    camera.right = normalize(camera.right) # normalizando o vetor

    camera.up = np.cross(camera.right, camera.forward)
    camera.up = normalize(camera.up)

    #matrix de rotação
    rotation = np.array([
        camera.right,
        camera.up,
        camera.forward
    ])

    #traslação 
    transformation = vertices -camera.position
    #rotação
    transformation = transformation @ rotation.T # @ é usado para operações entre matrizes AxB^t
    return transformation

def update_camera(camera):
    #coordendas esféricas
    x = camera.radius * math.cos(camera.pitch) * math.cos(camera.yaw)

    y= camera.radius * math.sin(camera.pitch)

    z = camera.radius * math.cos(camera.pitch) * math.sin(camera.yaw)

    #posição orbital

    camera.position = camera.target + np.array([x,y,z], type=float)


@dataclass
class Camera:
    #posição da camera
    position: np.ndarray

    #eixo de rotação 
    forward: np.ndarray
    up: np.ndarray
    right: np.ndarray

    #onde ela está olhando
    target: np.ndarray

    yaw: float #rotação horizontal 
    pitch: float #rotação
    radius: float