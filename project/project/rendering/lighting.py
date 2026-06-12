import numpy as np

def normalize(v):

    norm = np.linalg.norm(v)

    if norm < 1e-6:
        return v

    return v / norm


def phong(face, light_position):

    N = normalize(face.normal)

    L = normalize( light_position - face.center)

    V = normalize( -face.center )

    ambient = 0.2

    diffuse = max( 0.0, np.dot(N, L) )

    R = ( 2 * np.dot(N, L) * N - L)

    R = normalize(R)

    shininess = 8

    specular = max( 0.0, np.dot(R, V))

    specular = specular ** shininess

    intensity = ( ambient + 0.5 * diffuse + 0.5* specular )

    intensity = min( intensity, 1.0 )

    r = int(face.color[0] * intensity)
    g = int(face.color[1] * intensity)
    b = int(face.color[2] * intensity)

    face.shaded_color = ( r, g, b )

def vertex_lambert( position, normal, light_position, color):

    L = light_position - position

    norm = np.linalg.norm(L)

    if norm < 1e-6:
        return color

    L = L / norm

    diffuse = max( 0.0, np.dot(normal, L) )

    ambient = 0.2

    intensity = ( ambient + 0.8 * diffuse )

    intensity = min( intensity, 1.0 )

    return (
        int(color[0] * intensity),
        int(color[1] * intensity),
        int(color[2] * intensity)
    )

def vertex_phong( position, normal, light_position, color):

    N = normalize(normal)

    L = light_position - position

    norm = np.linalg.norm(L)

    if norm < 1e-6:
        return color

    L = L / norm

    # câmera está na origem do SCC
    V = normalize(-position)

    ambient = 0.2

    ndotl = np.dot(N, L)

    diffuse = max(0.0, ndotl)

    R = (
        2 * np.dot(N, L) * N
        - L
    )

    R = normalize(R)

    shininess = 16

    specular = max(
        0.0,
        np.dot(R, V)
    )

    specular = specular ** shininess

    intensity = (
        ambient
        + 0.6 * diffuse
        + 0.4 * specular
    )

    intensity = min(
        intensity,
        1.0
    )

    return (
        int(color[0] * intensity),
        int(color[1] * intensity),
        int(color[2] * intensity)
    )