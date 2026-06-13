import sys
import os

# Garante que o Python encontre os ficheiros no diretório atual
sys.path.append(os.getcwd())

from Renderer3D import Renderer3D
from Mesh import Mesh

# =========================================================================
# IMPORTAÇÃO DOS SÓLIDOS (Peças modeladas e Tabuleiro)
# =========================================================================
from Torre import torre
from Pino import pino
from Rainha import rainha
from Rei import rei
from Dama import dama
from TabuleiroBezier import tabuleiro

def compor_cena():
    # Cria a malha mestre que vai conter todo o "mundo"
    cena = Mesh()

    # =========================================================================
    # FATORES DE ESCALA INDIVIDUAIS
    # =========================================================================
    escala_torre  = 1.0   
    escala_pino   = 1.0  
    escala_rainha = 1.0   
    escala_rei    = 1.0   
    escala_dama   = 1.0   

    # =========================================================================
    # POSICIONAMENTO DO TABULEIRO
    # =========================================================================
    # O tabuleiro já é gerado centrado na origem (0,0,0)
    cena.merge(tabuleiro)

    # =========================================================================
    # POSICIONAMENTO DAS PEÇAS (Ajustando a altura Y para acompanhar a onda)
    # =========================================================================

    # 1. TORRE (Extrema esquerda)
    torre.scale(escala_torre, escala_torre, escala_torre)
    torre.translate(-3.0, 1.5, -3.0)
    cena.merge(torre)

    # 2. PINO / PEÃO (Centro-esquerda) 
    pino.scale(escala_pino, escala_pino, escala_pino)
    pino.translate(-2.0, 1.5, 3.0)
    cena.merge(pino)

    # 3. RAINHA (Centro exato)
    rainha.scale(escala_rainha, escala_rainha, escala_rainha)
    rainha.translate(3.0, 1.5, -2.0)
    cena.merge(rainha)

    # 4. REI (Centro-direita) 
    rei.scale(escala_rei, escala_rei, escala_rei)
    rei.translate(2.0, 1.5, 2.0)
    cena.merge(rei)

    # 5. DAMA (Extrema direita) 
    dama.scale(escala_dama, escala_dama, escala_dama)
    dama.translate(-0.5, 1.5, -0.5)
    cena.merge(dama)

    return cena

if __name__ == "__main__":
    # Gera a cena completa com todas as peças e o tabuleiro
    cena_final = compor_cena()

    renderer = Renderer3D()
    renderer.render_faces(cena_final)

    # Opcional: Exporta a cena final inteira para um único ficheiro OBJ
    cena_final.export_obj("Contrução das Peças/listaVerticesFaces/cenaFinal.obj")