from PIL import Image
import glob

# Coleta todas as imagens geradas em ordem sequencial
frames_arquivos = sorted(glob.glob("animacao_cubo/frame_*.png"))
frames = [Image.open(f) for f in frames_arquivos]

# Salva todas juntas em um único arquivo GIF em loop
frames[0].save(
    "cubo_girando.gif",
    save_all=True,
    append_images=frames[1:],
    duration=50, # Tempo de transição entre os frames em milissegundos
    loop=0       # Significa loop infinito
)
print("GIF 'cubo_girando.gif' gerado com sucesso!")