# images.py
import os
from PIL import Image
import customtkinter as ctk
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):  # Executando como .exe via PyInstaller
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))  # utils/




def load_icons():
    """
    Carrega as imagens necessárias e retorna um dicionário
    com as instâncias de CTkImage.
    """
    # Subir um nível para acessar o diretório raiz (sisatas)
    base_path = os.path.dirname(get_base_path())  # Agora base_path aponta para "sisatas"


    # Abra as imagens com PIL.Image.open(...)
    caminho_buscar = os.path.join(base_path, "assets", "img", "Buscar_Fala.png")
    imagem_buscar = Image.open(caminho_buscar)

    icon_buscar = ctk.CTkImage(
        dark_image=imagem_buscar,
        light_image=imagem_buscar,
        size=(20, 20)
    )

    caminho_atas = os.path.join(base_path, "assets", "img", "Listar_Atas.png")
    imagem_atas = Image.open(caminho_atas)

    icon_atas = ctk.CTkImage(
        dark_image=imagem_atas,
        light_image=imagem_atas,
        size=(20, 20)
    )

    caminho_secretarias = os.path.join(base_path, "assets", "img", "Secretarias.png")
    imagem_secretarias = Image.open(caminho_secretarias)

    icon_secretarias = ctk.CTkImage(
        dark_image=imagem_secretarias,
        light_image=imagem_secretarias,
        size=(20, 20)
    )

    caminho_secretarios = os.path.join(base_path,"assets", "img",  "Secretarios.png")
    imagem_secretarios = Image.open(caminho_secretarios)

    icon_secretarios = ctk.CTkImage(
        dark_image=imagem_secretarios,
        light_image=imagem_secretarios,
        size=(20, 20)
    )

    caminho_importar_dados = os.path.join(base_path,"assets", "img",  "Importar_Dados.png")
    imagem_importar_dados = Image.open(caminho_importar_dados)

    icon_importar = ctk.CTkImage(
        dark_image=imagem_importar_dados,
        light_image=imagem_importar_dados,
        size=(20, 20)
    )

    caminho_exportar_dados = os.path.join(base_path, "assets", "img", "Exportar_Dados.png")
    imagem_exportar_dados = Image.open(caminho_exportar_dados)
 
    icon_exportar = ctk.CTkImage(
        dark_image=imagem_exportar_dados,
        light_image=imagem_exportar_dados,
        size=(20, 20)
    )

    caminho_logo_principal= os.path.join(base_path,"assets", "img",  "logo_principal.png")
    imagem_logo_principal = Image.open(caminho_logo_principal)
 
    icon_logo_principal = ctk.CTkImage(
        dark_image=imagem_logo_principal,
        light_image=imagem_logo_principal,
        size=(265, 80)
    )

    caminho_adicionar= os.path.join(base_path,"assets", "img", "Adicionar.png")
    imagem_adicionar = Image.open(caminho_adicionar)
 
    icon_adicionar = ctk.CTkImage(
        dark_image=imagem_adicionar,
        light_image=imagem_adicionar,
        size=(14, 14)
    )

    caminho_calendar = os.path.join(base_path,"assets", "img", "calendar.png")
    imagem_calendar = Image.open(caminho_calendar)

    icon_calendar = ctk.CTkImage(
        dark_image=imagem_calendar,
        light_image=imagem_calendar,
        size=(14, 14)
    )

    caminho_seta_para_baixo = os.path.join(base_path,"assets", "img","seta_para_baixo.png")
    imagem_seta_para_baixo = Image.open(caminho_seta_para_baixo)

    icon_seta_para_baixo = ctk.CTkImage(
        dark_image=imagem_seta_para_baixo,
        light_image=imagem_seta_para_baixo,
        size=(14, 14)
    )

    # Retorna tudo em um dicionário organizado.
    return {
        "buscar": icon_buscar,
        "atas": icon_atas,
        "secretarias": icon_secretarias,
        "secretarios": icon_secretarios,
        "importar": icon_importar,
        "exportar": icon_exportar,
        "logo_principal": icon_logo_principal,
        "adicionar": icon_adicionar,
        "calendar": icon_calendar,
        "seta_para_baixo": icon_seta_para_baixo
    }
