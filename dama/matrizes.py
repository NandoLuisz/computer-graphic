import numpy as np

def translation_matrix(tx, ty, tz):
    return np.array([
        [1.0, 0.0, 0.0,  tx],
        [0.0, 1.0, 0.0,  ty],
        [0.0, 0.0, 1.0,  tz],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=float)

def scale_matrix(sx, sy, sz):
    return np.array([
        [ sx, 0.0, 0.0, 0.0],
        [0.0,  sy, 0.0, 0.0],
        [0.0, 0.0,  sz, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=float)

def rotation_y_matrix(angle_degrees):
    rad = np.radians(angle_degrees)
    cos_t = np.cos(rad)
    sin_t = np.sin(rad)
    return np.array([
        [ cos_t, 0.0, sin_t, 0.0],
        [   0.0, 1.0,   0.0, 0.0],
        [-sin_t, 0.0, cos_t, 0.0],
        [   0.0, 0.0,   0.0, 1.0]
    ], dtype=float)

def compute_camera_lookat(eye, target=np.array([0.0, 0.0, 0.0]), up=np.array([0.0, 0.0, 1.0])):
    eye = np.array(eye, dtype=float)
    
    # Vetor Z da câmera (aponta na direção oposta ao alvo)
    zc = eye - target
    zc /= np.linalg.norm(zc)
    
    # Vetor X da câmera (ortogonal ao 'up' e ao 'zc')
    xc = np.cross(up, zc)
    xc /= np.linalg.norm(xc)
    
    # Vetor Y da câmera (completa a base ortonormal)
    yc = np.cross(zc, xc)
    
    R = np.array([
        [xc[0], xc[1], xc[2], 0.0],
        [yc[0], yc[1], yc[2], 0.0],
        [zc[0], zc[1], zc[2], 0.0],
        [   0.0,   0.0,   0.0, 1.0]
    ], dtype=float)
    
    T = translation_matrix(-eye[0], -eye[1], -eye[2])
    return R @ T

def perspective_projection_matrix(fov, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    return np.array([
        [f / aspect, 0.0,                               0.0,                                     0.0],
        [       0.0,   f,                               0.0,                                     0.0],
        [       0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far)],
        [       0.0, 0.0,                              -1.0,                                     0.0]
    ], dtype=float)

def rotation_x_matrix(angle_degrees):
    rad = np.radians(angle_degrees)
    cos_t = np.cos(rad)
    sin_t = np.sin(rad)
    return np.array([
        [1.0,   0.0,    0.0, 0.0],
        [0.0, cos_t, -sin_t, 0.0],
        [0.0, sin_t,  cos_t, 0.0],
        [0.0,   0.0,    0.0, 1.0]
    ], dtype=float)

def rotation_z_matrix(angle_degrees):
    rad = np.radians(angle_degrees)
    cos_t = np.cos(rad)
    sin_t = np.sin(rad)
    return np.array([
        [cos_t, -sin_t, 0.0, 0.0],
        [sin_t,  cos_t, 0.0, 0.0],
        [  0.0,    0.0, 1.0, 0.0],
        [  0.0,    0.0, 0.0, 1.0]
    ], dtype=float)