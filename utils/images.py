# images.py
import os
from PIL import Image
import customtkinter as ctk
import sys

def get_base_path():
    """ Obtém o caminho correto para os arquivos, seja localmente ou no executável """
    if getattr(sys, 'frozen', False):  # Se estiver rodando como .exe
        return os.path.join(sys._MEIPASS, "assets", "img")
    
    # Caminho local no ambiente de desenvolvimento
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")



def load_icons():
    """
    Carrega as imagens necessárias e retorna um dicionário
    com as instâncias de CTkImage.
    """
    # Subir um nível para acessar o diretório raiz (sisatas)
    base_path = get_base_path()
    caminho_buscar = os.path.join(base_path, "Buscar_Fala.png")

    if not os.path.exists(caminho_buscar):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_buscar}")

    imagem_buscar = Image.open(caminho_buscar)
 

    icon_buscar = ctk.CTkImage(
        dark_image=imagem_buscar,
        light_image=imagem_buscar,
        size=(20, 20)
    )

    caminho_atas = os.path.join(base_path, "Listar_Atas.png")
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

    caminho_importar_dados = os.path.join(base_path,  "Importar_Dados.png")
    imagem_importar_dados = Image.open(caminho_importar_dados)

    icon_importar = ctk.CTkImage(
        dark_image=imagem_importar_dados,
        light_image=imagem_importar_dados,
        size=(20, 20)
    )

    caminho_exportar_dados = os.path.join(base_path,  "Exportar_Dados.png")
    imagem_exportar_dados = Image.open(caminho_exportar_dados)
 
    icon_exportar = ctk.CTkImage(
        dark_image=imagem_exportar_dados,
        light_image=imagem_exportar_dados,
        size=(20, 20)
    )

    caminho_logo_principal= os.path.join(base_path, "logo_principal.png")
    imagem_logo_principal = Image.open(caminho_logo_principal)
 
    icon_logo_principal = ctk.CTkImage(
        dark_image=imagem_logo_principal,
        light_image=imagem_logo_principal,
        size=(222, 90)
    )

    caminho_adicionar= os.path.join(base_path,"Adicionar.png")
    imagem_adicionar = Image.open(caminho_adicionar)
 
    icon_adicionar = ctk.CTkImage(
        dark_image=imagem_adicionar,
        light_image=imagem_adicionar,
        size=(14, 14)
    )

    caminho_calendar = os.path.join(base_path,"calendar.png")
    imagem_calendar = Image.open(caminho_calendar)

    icon_calendar = ctk.CTkImage(
        dark_image=imagem_calendar,
        light_image=imagem_calendar,
        size=(14, 14)
    )

    caminho_seta_para_baixo = os.path.join(base_path,"seta_para_baixo.png")
    imagem_seta_para_baixo = Image.open(caminho_seta_para_baixo)

    icon_seta_para_baixo = ctk.CTkImage(
        dark_image=imagem_seta_para_baixo,
        light_image=imagem_seta_para_baixo,
        size=(14, 14)
    )

    caminho_voltar = os.path.join(base_path,"voltar.png")
    imagem_voltar = Image.open(caminho_voltar)

    icon_voltar = ctk.CTkImage(
        dark_image=imagem_voltar,
        light_image=imagem_voltar,
        size=(16, 16)
    )

    caminho_pesquisar = os.path.join(base_path,"pesquisar.png")
    imagem_pesquisar = Image.open(caminho_pesquisar)

    icon_pesquisar = ctk.CTkImage(
        dark_image=imagem_pesquisar,
        light_image=imagem_pesquisar,
        size=(20, 20)
    )

    caminho_editar = os.path.join(base_path,"editar.png")
    imagem_editar = Image.open(caminho_editar)

    icon_editar = ctk.CTkImage(
        dark_image=imagem_editar,
        light_image=imagem_editar,
        size=(18, 20)
    )

    caminho_deletar = os.path.join(base_path,"deletar.png")
    imagem_deletar = Image.open(caminho_deletar)

    icon_deletar = ctk.CTkImage(
        dark_image=imagem_deletar,
        light_image=imagem_deletar,
        size=(20, 20)
    )

    caminho_exportar = os.path.join(base_path,"exportar.png")
    imagem_exportar = Image.open(caminho_exportar)

    icon_exportar = ctk.CTkImage(
        dark_image=imagem_exportar,
        light_image=imagem_exportar,
        size=(18, 19)
    )

    caminho_desativar = os.path.join(base_path,"desativar.png")
    imagem_desativar = Image.open(caminho_desativar)

    icon_desativar = ctk.CTkImage(
        dark_image=imagem_desativar,
        light_image=imagem_desativar,
        size=(18, 21)
    )

    caminho_ativar = os.path.join(base_path,"ativar.png")
    imagem_ativar = Image.open(caminho_ativar)

    icon_ativar = ctk.CTkImage(
        dark_image=imagem_ativar,
        light_image=imagem_ativar,
        size=(18, 21)
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
        "seta_para_baixo": icon_seta_para_baixo,
        "voltar": icon_voltar,
        "pesquisar": icon_pesquisar,
        "editar": icon_editar,
        "deletar": icon_deletar,
        "desativar": icon_desativar,
        "ativar": icon_ativar
    }
