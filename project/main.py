import numpy as np
from PIL import Image
import os

from matrizes import translation_matrix, scale_matrix, rotation_x_matrix, rotation_y_matrix, compute_camera_lookat, perspective_projection_matrix
from malhas import create_cube
from pipeline import is_face_visible, compute_lighting, to_viewport, rasterize_triangle

def main():
    # Criar uma pasta para salvar a animação
    os.makedirs("animacao_cubo", exist_ok=True)

    # Resolução fixa para a animação (128x128 ou 512x512 para não demorar muito)
    w, h = 512, 512
    
    # Configurações fixas de Câmera e Luz
    posicao_camera = [6.0, 7.0, 5.0]
    V = compute_camera_lookat(eye=posicao_camera, target=[0, 0, 0], up=[0, 0, 1])
    
    posicao_luz_mundo = np.array([5.0, 10.0, 8.0, 1.0])
    light_cam = (V @ posicao_luz_mundo)[:3]

    # Criamos o cubo original na origem uma única vez
    cubo_base = create_cube(color=[0.1, 0.6, 0.9])

    # Quantidade de frames da animação (ex: 24 frames para uma rotação parcial)
    total_frames = 24
    print(f"Iniciando a renderização da animação ({total_frames} frames)...")

    for frame in range(total_frames):
        # O ângulo muda a cada frame baseado no número do frame atual
        angulo_atual = frame * (360.0 / total_frames)
        
        # Alocar buffers limpos (fundo preto) para ESTE frame específico
        z_buffer = np.full((h, w), np.inf, dtype=float)
        frame_buffer = np.zeros((h, w, 3), dtype=float)

        # Matrizes do mundo atualizadas dinamicamente
        T = translation_matrix(0, 0, 0)
        S = scale_matrix(2.5, 2.5, 2.5)
        R_y = rotation_y_matrix(angulo_atual)  # Mexendo no ângulo Y a cada iteração!
        R_x = rotation_x_matrix(20)            # Inclinação fixa em X para dar perspectiva
        
        M_mundo = T @ R_x @ R_y @ S

        # Criar uma cópia dos vértices para não estragar o modelo original
        vertices_transformados = (M_mundo @ cubo_base.vertices.T).T

        # Mapear vértices para o espaço da Câmera
        v_cam = (V @ vertices_transformados.T).T

        # --- EXECUÇÃO DO PIPELINE PADRÃO ---
        for face in cubo_base.faces:
            idx0, idx1, idx2 = face
            
            edge1 = v_cam[idx1][:3] - v_cam[idx0][:3]
            edge2 = v_cam[idx2][:3] - v_cam[idx0][:3]
            face_normal_cam = np.cross(edge1, edge2)
            norm = np.linalg.norm(face_normal_cam)
            if norm > 0: face_normal_cam /= norm

            if is_face_visible(v_cam[idx0], face_normal_cam):
                c0 = compute_lighting(v_cam[idx0], face_normal_cam, cubo_base.color, light_cam)
                c1 = compute_lighting(v_cam[idx1], face_normal_cam, cubo_base.color, light_cam)
                c2 = compute_lighting(v_cam[idx2], face_normal_cam, cubo_base.color, light_cam)

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

        # Salvar o frame atual na pasta com numeração sequencial (ex: frame_000.png, frame_001.png)
        img_data = (frame_buffer * 255).astype(np.uint8)
        img = Image.fromarray(img_data, 'RGB')
        img.save(f"animacao_cubo/frame_{frame:03d}.png")
        print(f"Frame {frame+1}/{total_frames} renderizado.")

    print("\nPronto! Todos os frames foram salvos na pasta 'animacao_cubo'.")

if __name__ == "__main__":
    main()