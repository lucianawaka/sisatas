# images.py
import os
from PIL import Image
import customtkinter as ctk

def load_icons():
    """
    Carrega as imagens necessárias e retorna um dicionário
    com as instâncias de CTkImage.
    """
    # Ajuste estes caminhos conforme sua estrutura de pastas
    base_path = os.path.join("assets", "img")



    # Abra as imagens com PIL.Image.open(...)
    caminho_buscar = os.path.join(base_path, "Buscar Fala.png")
    imagem_buscar = Image.open(caminho_buscar)

    icon_buscar = ctk.CTkImage(
        dark_image=imagem_buscar,
        light_image=imagem_buscar,
        size=(20, 20)
    )

    caminho_atas = os.path.join(base_path, "Listar Atas.png")
    imagem_atas = Image.open(caminho_atas)

    icon_atas = ctk.CTkImage(
        dark_image=imagem_atas,
        light_image=imagem_atas,
        size=(20, 20)
    )

    caminho_secretarias = os.path.join(base_path, "Secretarias.png")
    imagem_secretarias = Image.open(caminho_secretarias)

    icon_secretarias = ctk.CTkImage(
        dark_image=imagem_secretarias,
        light_image=imagem_secretarias,
        size=(20, 20)
    )

    caminho_secretarios = os.path.join(base_path, "Secretarios.png")
    imagem_secretarios = Image.open(caminho_secretarios)

    icon_secretarios = ctk.CTkImage(
        dark_image=imagem_secretarios,
        light_image=imagem_secretarios,
        size=(20, 20)
    )

    caminho_importar_dados = os.path.join(base_path, "Importar Dados.png")
    imagem_importar_dados = Image.open(caminho_importar_dados)

    icon_importar = ctk.CTkImage(
        dark_image=imagem_importar_dados,
        light_image=imagem_importar_dados,
        size=(20, 20)
    )

    caminho_exportar_dados = os.path.join(base_path, "Exportar Dados.png")
    imagem_exportar_dados = Image.open(caminho_exportar_dados)
 
    icon_exportar = ctk.CTkImage(
        dark_image=imagem_exportar_dados,
        light_image=imagem_exportar_dados,
        size=(20, 20)
    )

    # Retorna tudo em um dicionário organizado.
    return {
        "buscar": icon_buscar,
        "atas": icon_atas,
        "secretarias": icon_secretarias,
        "secretarios": icon_secretarios,
        "importar": icon_importar,
        "exportar": icon_exportar
    }
