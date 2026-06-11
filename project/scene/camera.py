from dataclasses import dataclass
import numpy as np
import math

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def World_to_camera(vertices, camera):

    relative = camera.target - camera.position
    camera.forward = normalize(relative)

    if abs(camera.forward[1]) > 0.99:
        world_up = np.array([1,0,0], dtype=float)
    else:
        world_up = np.array([0,1,0], dtype=float)

    camera.right = np.cross(
        camera.forward,
        world_up
    )

    camera.right = normalize(
        camera.right
    )

    camera.up = np.cross(
        camera.right,
        camera.forward
    )

    camera.up = normalize(
        camera.up
    )

    rotation = np.array([
        camera.right,
        camera.up,
        camera.forward
    ])

    transformation = vertices - camera.position

    transformation = (
        transformation
        @ rotation.T
    )

    return transformation, rotation

def update_camera(camera):
    #coordendas esféricas
    x = camera.radius * math.cos(camera.pitch) * math.cos(camera.yaw)

    y= camera.radius * math.sin(camera.pitch)

    z = camera.radius * math.cos(camera.pitch) * math.sin(camera.yaw)

    #posição orbital

    camera.position = camera.target + np.array([x,y,z], dtype=float)


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