import math
import numpy as np

# realiza as operações de transformações que vimos em aula, o programa realiza operações matriciais 

def translate(vertices, position):
    return vertices + position

def rotate_x(vetices, angle):
    angle = math.radians(angle)
    rotation_matrix=np.array([
        [1,                0,               0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])
    return vetices @ rotation_matrix.T # multiplicação matricial A X B^T

def rotate_y(vertices, angle):
    angle= math.radians(angle)
    rotation_matrix = np.array([
        [math.cos(angle), 0 , math.sin(angle)],
        [0,              1,                 0],
        [-math.sin(angle), 0 ,math.cos(angle)]     
    ])
    return vertices @rotation_matrix.T

def rotate_z(vertices, angle):
    angle = math.radians(angle)
    rotation_matrix = np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle),  math.cos(angle), 0],
        [0,                0,               1]
    ])
    return vertices @ rotation_matrix.T

def rotation(vertices, rotation):
    vertices = rotate_x(vertices, rotation[0])
    vertices = rotate_y(vertices, rotation[1])
    vertices = rotate_z(vertices, rotation[2])

    return vertices


def scale(vertices, factor):
    scale_matrix= np.array([
        [factor, 0, 0],
        [0, factor, 0],
        [0, 0, factor]
    ])
    return vertices @ scale_matrix.T