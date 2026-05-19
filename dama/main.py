import numpy as np
from PIL import Image

from matrizes import translation_matrix, scale_matrix, rotation_x_matrix, rotation_y_matrix, compute_camera_lookat, perspective_projection_matrix
from malhas import create_checker_piece
from pipeline import is_face_visible, compute_lighting, to_viewport, rasterize_triangle

def main():
    resolutions = [(128, 128), (512, 512), (1024, 1024)]
    
    # Instancia a peça de dama vermelha
    dama = create_checker_piece(color=[0.8, 0.1, 0.1])
    
    # Matriz do mundo: Escala para dar tamanho, inclina em X e Y para ver em perspectiva
    M_mundo = translation_matrix(0, 0, -1) @ scale_matrix(4.0, 4.0, 4.0) @ rotation_x_matrix(65) @ rotation_y_matrix(20)
    dama.vertices = (M_mundo @ dama.vertices.T).T
    dama.compute_normals()

    # Câmera e Luz posicionadas no espaço do mundo
    V = compute_camera_lookat(eye=[6.0, 7.0, 5.0], target=[0, 0, 0], up=[0, 0, 1])
    light_cam = (V @ np.array([5.0, 10.0, 8.0, 1.0]))[:3]

    # Loop para gerar as três imagens pedidas no trabalho
    for w, h in resolutions:
        print(f"Renderizando Dama {w}x{h}...")
        z_buffer = np.full((h, w), np.inf, dtype=float)
        frame_buffer = np.zeros((h, w, 3), dtype=float)

        v_cam = (V @ dama.vertices.T).T

        for face in dama.faces:
            idx0, idx1, idx2 = face
            
            edge1 = v_cam[idx1][:3] - v_cam[idx0][:3]
            edge2 = v_cam[idx2][:3] - v_cam[idx0][:3]
            face_normal_cam = np.cross(edge1, edge2)
            norm = np.linalg.norm(face_normal_cam)
            if norm > 0: face_normal_cam /= norm

            if is_face_visible(v_cam[idx0], face_normal_cam):
                c0 = compute_lighting(v_cam[idx0], face_normal_cam, dama.color, light_cam)
                c1 = compute_lighting(v_cam[idx1], face_normal_cam, dama.color, light_cam)
                c2 = compute_lighting(v_cam[idx2], face_normal_cam, dama.color, light_cam)

                P = perspective_projection_matrix(fov=60.0, aspect=w/h, near=0.1, far=50.0)
                v0_proj = P @ v_cam[idx0]
                v1_proj = P @ v_cam[idx1]
                v2_proj = P @ v_cam[idx2]

                v0_ndc = v0_proj[:3] / v0_proj[3]
                v1_ndc = v1_proj[:3] / v1_proj[3]
                v2_ndc = v2_proj[:3] / v2_proj[3]

                scr0 = to_viewport(v0_ndc, w, h)
                scr1 = to_viewport(v1_ndc, w, h)
                scr2 = to_viewport(v2_ndc, w, h)

                rasterize_triangle(scr0, scr1, scr2, c0, c1, c2, w, h, z_buffer, frame_buffer)

        img_data = (frame_buffer * 255).astype(np.uint8)
        img = Image.fromarray(img_data, 'RGB')
        img.save(f"dama_{w}x{h}.png")
        print(f"Salvo: dama_{w}x{h}.png")

if __name__ == "__main__":
    main()