import numpy as np

def is_face_visible(v0_cam, normal_cam):
    # No espaço da câmera, a câmera está em (0,0,0). O vetor de visão aponta do vértice para ela.
    view_dir = np.array([0.0, 0.0, 0.0]) - v0_cam[:3]
    view_norm = np.linalg.norm(view_dir)
    if view_norm > 0:
        view_dir /= view_norm
    return np.dot(normal_cam, view_dir) > 0.0

def compute_lighting(pos_cam, normal_cam, mesh_color, light_pos_cam):
    ka, kd, ks = 0.15, 0.65, 0.3
    shininess = 16.0
    
    Ia = np.array([1.0, 1.0, 1.0])
    Id = np.array([1.0, 1.0, 1.0])
    Is = np.array([1.0, 1.0, 1.0])
    
    N = normal_cam / np.linalg.norm(normal_cam)
    L = light_pos_cam - pos_cam[:3]
    L_norm = np.linalg.norm(L)
    if L_norm > 0: L /= L_norm
    
    V = -pos_cam[:3]
    V_norm = np.linalg.norm(V)
    if V_norm > 0: V /= V_norm
    
    # Vetor de reflexão perfeita R
    R = 2.0 * np.dot(N, L) * N - L
    R_norm = np.linalg.norm(R)
    if R_norm > 0: R /= R_norm
    
    ambient = ka * Ia * mesh_color
    diffuse = kd * Id * mesh_color * max(np.dot(N, L), 0.0)
    specular = ks * Is * (max(np.dot(R, V), 0.0) ** shininess)
    
    return np.clip(ambient + diffuse + specular, 0.0, 1.0)

def to_viewport(v_ndc, width, height):
    # Mapeia de [-1, 1] para [0, largura/altura] invertendo o Y de tela
    x_screen = int((v_ndc[0] + 1.0) * 0.5 * (width - 1))
    y_screen = int((1.0 - v_ndc[1]) * 0.5 * (height - 1))
    return [x_screen, y_screen, v_ndc[2]]

def rasterize_triangle(v0, v1, v2, c0, c1, c2, width, height, z_buffer, frame_buffer):
    min_x = max(int(min(v0[0], v1[0], v2[0])), 0)
    max_x = min(int(max(v0[0], v1[0], v2[0])), width - 1)
    min_y = max(int(min(v0[1], v1[1], v2[1])), 0)
    max_y = min(int(max(v0[1], v1[1], v2[1])), height - 1)

    x0, y0, z0 = v0
    x1, y1, z1 = v1
    x2, y2, z2 = v2

    denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(denom) < 1e-6:
        return

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # Pesos baricêntricos
            alpha = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / denom
            beta = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / denom
            gamma = 1.0 - alpha - beta

            # Se o ponto estiver contido no triângulo
            if alpha >= 0.0 and beta >= 0.0 and gamma >= 0.0:
                # Interpolação linear da profundidade corrigida
                z_interpolated = alpha * z0 + beta * z1 + gamma * z2

                # Teste clássico do Z-buffer (Coordenadas de tela: menor Z está mais perto)
                if z_interpolated < z_buffer[y, x]:
                    z_buffer[y, x] = z_interpolated
                    
                    # Interpolação Baricêntrica de Cores (Gouraud Shading)
                    pixel_color = alpha * c0 + beta * c1 + gamma * c2
                    frame_buffer[y, x] = pixel_color