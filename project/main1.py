import numpy as np
from PIL import Image  # Certifique-se de ter rodado: pip install pillow

# Importando seus módulos criados
from matrizes import translation_matrix, scale_matrix, rotation_y_matrix, compute_camera_lookat, perspective_projection_matrix
from malhas import create_cube
from pipeline import is_face_visible, compute_lighting, to_viewport, rasterize_triangle
from matrizes import translation_matrix, scale_matrix, rotation_x_matrix, rotation_y_matrix, rotation_z_matrix

def main():
    # 1. Configurar Resoluções exigidas pelo enunciado
    resolutions = [(128, 128), (512, 512), (1024, 1024)]
    
    # 2. Inicializar o Objeto de Teste (Cubo)
    # 2. Inicializar o Objeto de Teste (Cubo)
    cubo = create_cube(color=[0.1, 0.6, 0.9])
    
    # Criando as matrizes isoladas
    T = translation_matrix(0, 0, 0)
    S = scale_matrix(2.5, 2.5, 2.5)
    
    R_x = rotation_x_matrix(90) # Rotaciona 45 graus inclinando para frente/trás
    R_y = rotation_y_matrix(30) # Rotaciona 30 graus para os lados
    R_z = rotation_z_matrix(0)  # 0 graus (sem rotação no próprio eixo)
    
    # Combina tudo na ordem correta: Translação @ Rotações @ Escala
    M_mundo = T @ R_x @ R_y @ R_z @ S
    
    # Aplica as transformações nos vértices do cubo
    cubo.vertices = (M_mundo @ cubo.vertices.T).T
    cubo.compute_normals() # ESSENCIAL: Recalcula as normais baseadas na nova rotação! # Ajustar normais originais para o espaço do mundo

    # 3. Definir Câmera (LookAt) e Luz no Espaço do Mundo
    posicao_camera = [6.0, 7.0, 5.0]
    V = compute_camera_lookat(eye=posicao_camera, target=[0, 0, 0], up=[0, 0, 1])
    
    posicao_luz_mundo = np.array([5.0, 10.0, 8.0, 1.0])
    light_cam = (V @ posicao_luz_mundo)[:3] # Luz convertida para espaço da câmera

    # 4. Executar o Pipeline Gráfico por resolução
    for w, h in resolutions:
        print(f"Renderizando resolução: {w}x{h}...")
        
        # Alocar buffers de renderização limpos
        z_buffer = np.full((h, w), np.inf, dtype=float)
        frame_buffer = np.zeros((h, w, 3), dtype=float) # Inicia em preto [0, 0, 0]

        # Mapear vértices do objeto atual para o espaço da Câmera
        v_cam = (V @ cubo.vertices.T).T

        for idx, face in enumerate(cubo.faces):
            idx0, idx1, idx2 = face
            
            # Gerar a normal geométrica da face diretamente no espaço da câmera
            edge1 = v_cam[idx1][:3] - v_cam[idx0][:3]
            edge2 = v_cam[idx2][:3] - v_cam[idx0][:3]
            face_normal_cam = np.cross(edge1, edge2)
            norm = np.linalg.norm(face_normal_cam)
            if norm > 0: face_normal_cam /= norm

            # Backface Culling (eliminar polígonos ocultos usando a normal)
            if is_face_visible(v_cam[idx0], face_normal_cam):
                
                # Iluminação por vértice (Gouraud Shading)
                c0 = compute_lighting(v_cam[idx0], face_normal_cam, cubo.color, light_cam)
                c1 = compute_lighting(v_cam[idx1], face_normal_cam, cubo.color, light_cam)
                c2 = compute_lighting(v_cam[idx2], face_normal_cam, cubo.color, light_cam)

                # Matriz de Projeção Perspectiva
                P = perspective_projection_matrix(fov=60.0, aspect=w/h, near=0.1, far=50.0)
                
                v0_proj = P @ v_cam[idx0]
                v1_proj = P @ v_cam[idx1]
                v2_proj = P @ v_cam[idx2]

                # Divisão Homogênea (NDC - Coordenadas Normalizadas de Dispositivo)
                v0_ndc = v0_proj[:3] / v0_proj[3]
                v1_ndc = v1_proj[:3] / v1_proj[3]
                v2_ndc = v2_proj[:3] / v2_proj[3]

                # Mapeamento para coordenadas de pixels (Viewport)
                scr0 = to_viewport(v0_ndc, w, h)
                scr1 = to_viewport(v1_ndc, w, h)
                scr2 = to_viewport(v2_ndc, w, h)

                # Rasterizar triângulo calculando cor baricêntrica pixel a pixel
                rasterize_triangle(scr0, scr1, scr2, c0, c1, c2, w, h, z_buffer, frame_buffer)

        # Converter a matriz de float [0, 1] para bytes inteiros [0, 255]
        img_data = (frame_buffer * 255).astype(np.uint8)
        img = Image.fromarray(img_data, 'RGB')
        img.save(f"render_{w}x{h}.png")
        print(f"Salvo com sucesso: render_{w}x{h}.png")

if __name__ == "__main__":
    main()