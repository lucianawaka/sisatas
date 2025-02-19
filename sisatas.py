import customtkinter as ctk
import tkinter as tk
import os  # Importação necessária para usar funções de sistema de arquivos
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import textwrap
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import textwrap
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename
import shutil
from datetime import datetime
from tkinter import Toplevel
from tkhtmlview import HTMLLabel, HTMLScrolledText
from tkcalendar import DateEntry
from database.connection import get_connection, atualizar_banco
from database.models import create_tables
from controllers.secretaria import adicionar_secretaria, listar_secretarias, deletar_secretaria, get_secretaria_por_id, atualizar_secretaria
from controllers.secretario import adicionar_secretario, listar_secretarios, get_secretaria_by_secretario, ativar_secretario, desativar_secretario, editar_secretario, get_secretario_por_id
from controllers.ata import adicionar_ata, listar_atas, buscar_atas_por_descricao, deletar_ata, editar_ata, obter_dados_ata
from controllers.fala import adicionar_fala, listar_falas_por_ata, limpar_todas_as_entidades, atualizar_fala, deletar_fala
from utils.CustomDatePicker import CustomDatePicker
from utils.images import load_icons

from utils.CTkHTMLScrolledText import CTkHTMLScrolledText
from components.Fotter import Footer
from components.Botoes import Botoes
from components.Containers import Containers
from components.CriarAta import CriarAta

class MeetingManagerApp:
    def __init__(self, root):
        self.conn = get_connection()
        #atualizar_banco(self.conn)
        self.root = root
        self.root.title("Gerenciador de Atas")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        #self.root.update_idletasks()  # Garante que o tkinter atualize as dimensões da janela
        #self.root.geometry("1200x800")

        ctk.set_appearance_mode("light")  # Tema: "light", "dark", "system"
        ctk.set_default_color_theme("green")  # Cor principal do tema

        # Carregar icones
        self.icons = load_icons()
        self.setup_ui()

    def setup_ui(self):

        self.root.configure(bg="#FAFAFA")

        # Frame principal ocupando toda a janela
        main_container = ctk.CTkFrame(self.root, fg_color="#FAFAFA")
        main_container.pack(fill="both", expand=True)

        # Frame para conter título e botões no topo
        header_frame = ctk.CTkFrame(main_container, fg_color="#FAFAFA")
        header_frame.pack(fill="x", pady=(20, 10), padx=60)


    # ---------- Título ----------
        label_titulo = ctk.CTkLabel(
            header_frame,
            text="Gerenciador de Atas",
            text_color="#019000",
            font=("Montserrat", 36, "bold")
        )
        label_titulo.pack(pady=(0, 10))  # Pequeno espaçamento abaixo do título



        # ---------- Botões no topo ----------
        container_botoes = ctk.CTkFrame(header_frame, fg_color="#FAFAFA")
        container_botoes.pack(fill="x")  # Ocupa toda a largura, mas usaremos grid internamente

        # Configura cada coluna do grid
        #  - colunas 0 e 7 (as extremidades) terão weight=1 para empurrar os botões ao centro
        #  - colunas 1..6 ficam sem weight (weight=0), pois os botões terão largura fixa
        for i in range(8):
            container_botoes.grid_columnconfigure(i, weight=0)
        container_botoes.grid_columnconfigure(0, weight=1)
        container_botoes.grid_columnconfigure(7, weight=1)

        # Botão de Listar Atas
        botao_buscar = ctk.CTkButton(
            container_botoes,
            text="Buscar fala",
            image=self.icons["buscar"],  # pega o ícone do dicionário
            compound="left",
            width=168,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Montserrat", 16, "bold"),
            command=self.listar_atas
        )
        botao_buscar.grid(row=0, column=1, padx=5, pady=10)  # sem sticky="ew" para manter a largura fixa

        # Botão de Carregar Menu da Atas
        botao_listar_atas = ctk.CTkButton(
            container_botoes, 
            text="Lista de atas",
            image=self.icons["atas"],
            compound="left",
            width=168,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Montserrat", 16, "bold"),
            command=self.menu_atas  # callback
        )
        botao_listar_atas.grid(row=0, column=2, padx=5, pady=10)

        # Botão de Carregar Menu da Secretaria
        botao_secretarias = ctk.CTkButton(
            container_botoes, 
            text="Secretarias",
            image=self.icons["secretarias"],
            compound="left",
            width=168,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Montserrat", 16, "bold"),
            command=self.menu_secretaria  # callback
        )
        botao_secretarias.grid(row=0, column=3, padx=5, pady=10)

        # Botão de Carregar Menu da Secretarios
        botao_secretarios = ctk.CTkButton(
            container_botoes,
            text="Secretários",
            image=self.icons["secretarios"],
            compound="left",
            width=168,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Montserrat", 16, "bold"),
            command=self.menu_secretario  # callback
        )
        botao_secretarios.grid(row=0, column=4, padx=5, pady=10)

        # --- Botões Importar/Exportar (195x48) com borda verde ---
        botao_importar = ctk.CTkButton(
            container_botoes,
            text="Importar Dados",
            image=self.icons["importar"],
            compound="left",
            width=195,
            height=48,
            fg_color="white",           # Fundo branco
            border_width=2,            
            border_color="#33A532",     # Cor da borda
            text_color="#33A532",       # Texto verde
            hover_color="#E8F6EE",      # Exemplo de cor de hover
            font=("Montserrat", 16, "bold"),
            command=self.carregar_backup  # callback
        )
        botao_importar.grid(row=0, column=5, padx=5, pady=10)

        botao_exportar = ctk.CTkButton(
            container_botoes,
            text="Exportar Dados",
            image=self.icons["exportar"],
            compound="left",
            width=195,
            height=48,
            fg_color="white",
            border_width=2,
            border_color="#33A532",
            text_color="#33A532",
            hover_color="#E8F6EE",
            font=("Montserrat", 16, "bold"),
            command=self.realizar_backup  # callback
        )
        botao_exportar.grid(row=0, column=6, padx=5, pady=10)

        # Primeiro BLOCO EM BRANCO: “Criação de Ata”
        CriarAta.criar_ata(self, main_container)

      
        # ----------------------------------------------------------------
        # SEGUNDO BLOCO EM BRANCO: “Criação de fala”
        # ----------------------------------------------------------------
        card_fala = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        card_fala.pack(fill="x", padx=400, pady=(0, 10))

        frame_fala = ctk.CTkFrame(card_fala, fg_color="white")
        frame_fala.pack(fill="x",pady=(20, 20))

        label_fala = ctk.CTkLabel(
            frame_fala,
            text="Criação de fala",
            font=("Montserrat", 22, "bold"),
            text_color="#007E37"
        )
        label_fala.pack(anchor="w", padx=10, pady=(0, 5))

        # Frame para comboboxes
        row_fala_combos = ctk.CTkFrame(frame_fala, fg_color="white")
        row_fala_combos.pack(fill="x")

        self.combo_atas = ctk.CTkComboBox(
            row_fala_combos, 
            values=["Selecione uma Ata"], 
            dropdown_fg_color="white",
            button_color="#019000",
            button_hover_color="#007E37",
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            text_color="#333333",
            text_color_disabled="#333333",
            font=("Montserrat", 14),
            dropdown_font=("Montserrat", 14),
            width=400,
            height=48
        )
        self.combo_atas.pack(side="left", padx=10, pady=5)

        self.combo_secretarios = ctk.CTkComboBox(
            row_fala_combos, 
            values=["Selecione um Secretário"], 
            button_color="#019000",
            button_hover_color="#007E37",
            dropdown_fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            font=("Montserrat", 14),
            dropdown_font=("Montserrat", 14),
            text_color_disabled="#333333",
            text_color="#333333",
            width=480,
            height=48,
            
        )
        self.combo_secretarios.pack(side="left", padx=5, pady=5)


        # Frame onde ficará a caixa de texto e o botão
        row_fala_text = ctk.CTkFrame(frame_fala, fg_color="white")
        row_fala_text.pack(fill="x", pady=10)

        # Text area (pode ser um CTkTextbox, se você quiser algo simples)
        self.html_editor_fala = CTkHTMLScrolledText(
            row_fala_text,
            corner_radius=10,
            border_color="#CCCCCC",
            border_width=1,
            fg_color="white",
            html="",
            font=("Montserrat", 14),
            width=80,
            height=10
        )
        self.html_editor_fala.pack(fill="x", padx=10, expand=True)

        # Botão Adicionar Fala, ancorado à direita
        botao_adicionar_fala = ctk.CTkButton(
            row_fala_text, 
            text="Adicionar Fala",
            image=self.icons["adicionar"],
            fg_color="#019000",
            text_color="#FFFFFF",
            hover_color="#007E37",
            width=500,
            height=48,
            corner_radius=8,
            font=("Montserrat", 16, "bold"),
            command=self.adicionar_fala
        )
        botao_adicionar_fala.pack(side="right", pady=(10, 5), padx=10)

        Footer.footer_container(self, main_container, self.icons["logo_principal"])

        self.atualizar_comboboxes()



    def return_to_main_menu(self):
        self.clear_content_frame()  # Limpa os widgets da tela de listar atas.
        self.setup_ui()  # Recria o menu principal.


    def clear_content_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def atualizar_comboboxes(self):
        try:
            # Atualizar as secretarias
            secretarias = listar_secretarias(self.conn)
            if hasattr(self, "combo_secretarias") and self.combo_secretarias.winfo_exists():
                self.combo_secretarias.configure(values=[s[1] for s in secretarias])

            # Atualizar secretários com nome e secretaria
            secretarios = listar_secretarios(self.conn)
            valores_combo_secretarios = [
                f"{s[1]} ({get_secretaria_by_secretario(self.conn, s[1])})" for s in secretarios
            ]
            if hasattr(self, "combo_secretarios") and self.combo_secretarios.winfo_exists():
                self.combo_secretarios.configure(values=valores_combo_secretarios)
            # Atualizar atas no ComboBox
            atas = listar_atas(self.conn)

            # Ordenar as atas pelo ID em ordem decrescente
            atas_ordenadas = sorted(atas, key=lambda x: x[0], reverse=True)

            # Criar a lista formatada para exibição no ComboBox
            valores_combo_atas = [f"{a[1]} - {a[2]}" for a in atas_ordenadas]

            # Atualizar as opções disponíveis no ComboBox
            self.combo_atas.configure(values=valores_combo_atas)

            # Definir a primeira opção como valor selecionado ou um padrão
            if valores_combo_atas:
                self.combo_atas.set(valores_combo_atas[0])  # Selecionar o primeiro valor
            else:
                self.combo_atas.set("Selecione uma Ata")  # Valor padrão caso a lista esteja vazia
        except Exception as e:
            print(f"Erro ao atualizar comboboxes: {e}")

    # Função para realizar backup
    def realizar_backup(self):
        try:
            # Abrir janela para o usuário selecionar a pasta
            pasta_selecionada = askdirectory(title="Selecione a pasta para salvar os dados")
            
            if not pasta_selecionada:
                # Caso o usuário cancele a seleção
                messagebox.showwarning("Exportar dados", "Nenhuma pasta foi selecionada.")
                return

            # Gerar nome do arquivo de backup com data e hora
            nome_backup = f"backup_atas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

            # Caminho completo para salvar o backup
            caminho_backup = f"{pasta_selecionada}/{nome_backup}"

            # Criar backup do banco de dados
            shutil.copy("banco_de_dados_atas.db", caminho_backup)
            messagebox.showinfo("Backup", f"Dados salvos com sucesso em: {caminho_backup}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar backup: {e}")


    # Carregar o Backup
    def carregar_backup(self):
        try:
            # Abrir janela para o usuário selecionar o arquivo de backup
            arquivo_backup = askopenfilename(
                title="Selecione o arquivo de backup",
                filetypes=[("Banco de Dados", "*.db"), ("Todos os Arquivos", "*.*")]
            )

            if not arquivo_backup:
                # Caso o usuário cancele a seleção
                messagebox.showwarning("Importar dados", "Nenhum arquivo de backup foi selecionado.")
                return

            # Substituir o banco de dados principal pelo arquivo de backup
            caminho_principal = "banco_de_dados_atas.db"
            shutil.copy(arquivo_backup, caminho_principal)

            # Reiniciar a conexão para garantir que os dados sejam atualizados
            self.conn.close()
            self.conn = get_connection()

            # Atualizar a interface com os novos dados
            self.atualizar_comboboxes()
            messagebox.showinfo("Importar dados", "Backup carregado com sucesso! O sistema foi atualizado com os dados do backup.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao Importar dados: {e}")

    # Secretaria inicio 

    def adicionar_secretaria(self):
        nome = self.entrada_secretaria.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome da secretaria não pode estar vazio.")
            return
        try:
            adicionar_secretaria(self.conn, nome)
            self.entrada_secretaria.delete(0, ctk.END)
            self.atualizar_lista_secretarias()
            messagebox.showinfo("Sucesso", "Secretaria adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar secretaria: {e}")

    # def atualizar_lista_secretarias(self):
    #     for widget in self.lista_secretarias.winfo_children():
    #         widget.destroy()

    #     secretarias = listar_secretarias(self.conn)

    #     for secretaria in secretarias:
    #         frame = ctk.CTkFrame(self.lista_secretarias)
    #         frame.pack(fill="x", padx=5, pady=5)

    #         nome = f"{secretaria[1]}"

    #         ctk.CTkLabel(frame, text=nome).pack(side="left", padx=5)

    #         botao_editar = ctk.CTkButton(frame, text="Editar", command=lambda s_id=secretaria[0]: self.editar_secretaria(s_id), fg_color="#007bff", hover_color="#0056b3", text_color="#FFFFFF")
    #         botao_editar.pack(side="right", padx=5)

    #         botao_deletar = ctk.CTkButton(frame, text="Deletar", command=lambda s_id=secretaria[0]: self.deletar_secretaria(s_id), fg_color="#dc3545", hover_color="#b02a37", text_color="#FFFFFF")
    #         botao_deletar.pack(side="right", padx=5)


    def menu_secretaria(self):
        
        # Frame para o cabeçalho
        main_container, header_frame = Containers.container_pages(self)

        # Botão de voltar
        Botoes.btn_voltar(self, header_frame)

        # ----------------------------------------------------------------
        # PRIMEIRO BLOCO EM BRANCO: “Criação de Secretaria”
        # ----------------------------------------------------------------
        card_ata = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        card_ata.pack(fill="x", padx=400, pady=(20, 20))

        # ---------- Seção: Criação de Secretaria ----------
        section_ata = ctk.CTkFrame(card_ata, fg_color="white")
        section_ata.pack(fill="x", pady=(10, 10))

        label_ata = ctk.CTkLabel(
            section_ata,
            text="Adicionar Secretaria",
            font=("Montserrat", 22, "bold"),
            text_color="#007E37"
        )
        label_ata.pack(anchor="w", pady=(0, 5), padx=10)


        # Frame único para agrupar os campos em linha
        row_secretaria = ctk.CTkFrame(section_ata, fg_color="white")
        row_secretaria.pack(fill="x")

        # Campo "Cadastro da Secretaria"
        self.entrada_secretaria  = ctk.CTkEntry(
            row_secretaria, 
            placeholder_text="Nome da Secretaria", 
            width=380,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            font=("Montserrat", 16)
        )
        self.entrada_secretaria.pack(side="left", padx=15, pady=5)

        # Botão "+ Nova Secretaria" (fica à extrema direita)
        botao_adicionar_secretaria = ctk.CTkButton(
            row_secretaria, 
            image=self.icons["adicionar"],
            text="Adicionar",
            fg_color="#019000",
            text_color="#FFFFFF",
            hover_color="#007E37",
            compound="left",
            width=155,
            height=48,
            font=("Montserrat", 16, "bold"),
            command=self.adicionar_secretaria
        )
        botao_adicionar_secretaria.pack(side="right", padx=10, pady=5)


        # ----------------------------------------------------------------
        # SEGUNDO BLOCO EM BRANCO: Listar Secretarias
        # ----------------------------------------------------------------
        
        card_secretarias = ctk.CTkFrame(main_container, 
                                        fg_color="white",
                                        corner_radius=10,
                                        )
        card_secretarias.pack(fill="x", padx=400, pady=(0, 10))

        # Frame para o label da lista (primeira linha)
        label_frame_secretarias = ctk.CTkFrame(card_secretarias, fg_color="white")
        label_frame_secretarias.pack(fill="x", pady=(10, 0), anchor="w")

        label_lista_secretarias = ctk.CTkLabel(label_frame_secretarias, 
                                        text="Secretarias",
                                        font=("Montserrat", 22, "bold"),
                                        text_color="#007E37"  
                                        )
        label_lista_secretarias.pack(fill="none", anchor="w", padx=10, pady=(5, 10))
       
        # Frame para listagem de Secretarias
        frame_lista_secretarias = ctk.CTkFrame(  
                                        card_secretarias, 
                                        bg_color="white",
                                        fg_color="white"
                                        )
        frame_lista_secretarias.pack(fill="both", expand=True, pady=(0, 20), padx=10)

        self.lista_secretarias = ctk.CTkScrollableFrame(
                                    frame_lista_secretarias, 
                                    width=800, 
                                    height=400, 
                                    fg_color="white",
                                    border_color="#FFFFFF", 
                                    border_width=2, 
                                    corner_radius=10,
                                    scrollbar_button_color="#CACACA",
                                    scrollbar_fg_color="white",
                                    scrollbar_button_hover_color="#007E37",
                                    bg_color="white",
                                    label_fg_color="white",
                                    label_text_color="#007E37",
                                    label_font=("Montserrat", 16, "bold"),
                                    
                                    )
        self.lista_secretarias.pack(fill="both", expand=True)

        # Footer
        Footer.footer_container(self, main_container, self.icons["logo_principal"])
        self.atualizar_lista_secretarias()

    def adicionar_secretaria(self):
        nome = self.entrada_secretaria.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome da secretaria não pode estar vazio.")
            return
        try:
            adicionar_secretaria(self.conn, nome)
            self.entrada_secretaria.delete(0, ctk.END)
            self.atualizar_lista_secretarias()
            messagebox.showinfo("Sucesso", "Secretaria adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar secretaria: {e}")

    def atualizar_lista_secretarias(self):
        for widget in self.lista_secretarias.winfo_children():
            widget.destroy()

        secretarias = listar_secretarias(self.conn)

        for secretaria in secretarias:
            frame = ctk.CTkFrame(self.lista_secretarias,
                                    bg_color="white",
                                    fg_color="white",          # Background color
            )
            frame.pack(fill="x", padx=5, pady=5)

            nome = f"{secretaria[1]}"

            ctk.CTkLabel(frame, 
                         text=nome, 
                         font=("Montserrat", 16), 
                         text_color="#333333").pack(side="left", padx=5)

            botao_deletar = ctk.CTkButton(frame,  
                                          fg_color="#E7000B", 
                                          image=self.icons["deletar"], 
                                          text="Deletar", 
                                          hover_color="#B7070F", 
                                          text_color="#FFFFFF",
                                          font=("Montserrat", 16, "bold"),
                                          command=lambda s_id=secretaria[0]: self.deletar_secretaria(s_id)
            )
            botao_deletar.pack(side="right", padx=5)

            botao_editar = ctk.CTkButton(frame,
                                         fg_color="#00AAA7", 
                                         image=self.icons["editar"], 
                                         text="Editar", 
                                         hover_color="#009693", 
                                         text_color="#FFFFFF",
                                         font=("Montserrat", 16, "bold"),
                                         command=lambda s_id=secretaria[0]: self.editar_secretaria(s_id)
            )
            botao_editar.pack(side="right", padx=5)

    def editar_secretaria(self, secretaria_id):
        # Cria uma nova janela para edição
        janela_edicao = ctk.CTkToplevel(self.root)
        janela_edicao.title("Editar Secretaria")
        janela_edicao.geometry("800x300")
        janela_edicao.grab_set()
        
        # Centraliza a janela na tela
        largura_janela = 800
        altura_janela = 300
        largura_tela = janela_edicao.winfo_screenwidth()
        altura_tela = janela_edicao.winfo_screenheight()

        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2

        janela_edicao.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
        # Obtém o nome atual da secretaria do controller
        secretaria_atual = get_secretaria_por_id(self.conn, secretaria_id)

        if not secretaria_atual:
            messagebox.showerror("Erro", "Secretaria não encontrada.")
            janela_edicao.destroy()
            return

        nome_atual = secretaria_atual["nome"]
        
        # Frame principal
        frame_campos = ctk.CTkFrame(janela_edicao, fg_color="#FFFFFF", corner_radius=10)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=20)
        
            # Configuração de colunas e linhas no grid (para layout responsivo)
        for i in range(5):
            frame_campos.grid_columnconfigure(i, weight=1)
        frame_campos.grid_rowconfigure(0, weight=0)
           # Título
        label_titulo = ctk.CTkLabel(
            frame_campos,
            text="Edite a Secretaria:",
            font=("Montserrat", 22, "bold"),
            text_color="#007E37"
        )
        label_titulo.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
 
        # Label e Entry para nome da Secretaria
        label_nome = ctk.CTkLabel(
            frame_campos,
            text="Nome da Secretaria:",
            font=("Montserrat", 14, "bold"),
            text_color="#007E37"
        )
        label_nome.grid(row=1, column=0, sticky="e", padx=10, pady=(5, 5))
        
        entrada_nome = ctk.CTkEntry(
                frame_campos,
                width=410,
                height=48,
                corner_radius=10,
                font=("Montserrat", 14),
                border_width=1,
                border_color="#CCCCCC",
                fg_color="white",
                text_color="#333333"
            )
        entrada_nome.insert(0, nome_atual)
        entrada_nome.grid(row=1, column=1, columnspan=3, sticky="ew", padx=10, pady=5)


        def salvar_edicao():
            novo_nome = entrada_nome.get().strip()
            if not novo_nome:
                messagebox.showerror("Erro", "O nome da secretaria não pode estar vazio.")
                return
            try:
                atualizar_secretaria(self.conn, secretaria_id, novo_nome)
                self.atualizar_lista_secretarias()
                messagebox.showinfo("Sucesso", "Secretaria atualizada com sucesso!")
                janela_edicao.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar secretaria: {e}")

        # Botão "Salvar" no canto inferior direito
        ctk.CTkButton(
            janela_edicao,
            text="Salvar",
            image=self.icons["editar"],  # Descomente esta linha se você tiver um ícone
            fg_color="#019000",
            text_color="#FFFFFF",
            hover_color="#007E37",
            compound="left",
            width=155,
            height=48,
            font=("Montserrat", 16, "bold"),
            command=salvar_edicao
        ).pack(pady=15, side="right", expand=True, padx=25)

    def deletar_secretaria(self, secretaria_id):
        resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja deletar esta secretaria?")
        if resposta:
            try:
                deletar_secretaria(self.conn, secretaria_id)
                self.atualizar_lista_secretarias()
                messagebox.showinfo("Sucesso", "Secretaria deletada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar secretaria: {e}")


    # Secretaria FIM
# Secretário
    def adicionar_secretario(self):
        nome = self.entrada_secretario.get()
        secretaria = self.combo_secretarias.get()
        if nome and secretaria:
            try:
                adicionar_secretario(self.conn, nome, secretaria)
                self.entrada_secretario.delete(0, ctk.END)
                self.atualizar_lista_secretarios()
                messagebox.showinfo("Sucesso", "Secretário adicionado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def atualizar_lista_secretarios(self):
        for widget in self.lista_secretarios.winfo_children():
            widget.destroy()

        secretarios = listar_secretarios(self.conn, incluir_inativos=True)

        for secretario in secretarios:
            frame = ctk.CTkFrame(self.lista_secretarios,
                                    bg_color="white",
                                    fg_color="white",          # Background color
                                )
            frame.pack(fill="x", padx=5, pady=5)

            nome = f"{secretario[1]} ({secretario[2]})"
            status = "Ativo" if secretario[3] == 1 else "Inativo"

            ctk.CTkLabel(frame, text=nome,
                         font=("Montserrat", 16), 
                         text_color="#333333").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=status,
                         font=("Montserrat", 14, "bold"), 
                         text_color="#333333").pack(side="left", padx=5)

            botao_editar = ctk.CTkButton(frame, 
                                        fg_color="#00AAA7", 
                                        image=self.icons["editar"], 
                                        text="Editar", 
                                        hover_color="#009693", 
                                        text_color="#FFFFFF",
                                        font=("Montserrat", 16, "bold"),
                                        command=lambda s_id=secretario[0]: self.editar_secretario(s_id))
            botao_editar.pack(side="right", padx=5)

            if secretario[3] == 1:
                botao = ctk.CTkButton(frame, text="Desativar", 
                                      image=self.icons["desativar"],
                                      fg_color="#ffa500", 
                                      hover_color="#cc8400", 
                                      text_color="#FFFFFF",
                                      font=("Montserrat", 16, "bold"),
                                      command=lambda s_id=secretario[0]: self.desativar_secretario(s_id)
                                      )
            else:
                botao = ctk.CTkButton(frame, text="Ativar", 
                                      command=lambda s_id=secretario[0]: self.ativar_secretario(s_id), 
                                      image=self.icons["ativar"],
                                      fg_color="#999999", 
                                      hover_color="#999999", 
                                      font=("Montserrat", 16, "bold"),
                                      text_color="#FFFFFF")

            botao.pack(side="right", padx=5)

    def ativar_secretario(self, secretario_id):
        try:
            ativar_secretario(self.conn, secretario_id)
            self.atualizar_lista_secretarios()
            messagebox.showinfo("Sucesso", "Secretário ativado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def desativar_secretario(self, secretario_id):
        try:
            desativar_secretario(self.conn, secretario_id)
            self.atualizar_lista_secretarios()
            messagebox.showinfo("Sucesso", "Secretário desativado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def get_lista_secretarias(self):
        """
        Retorna uma lista com os nomes das secretarias disponíveis no banco de dados.
        """
        try:
            # Obtém as secretarias usando a função listar_secretarias do controller
            secretarias = listar_secretarias(self.conn)
            return [s[1] for s in secretarias]  # Retorna apenas os nomes das secretarias
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar secretarias: {e}")
            return []

    def editar_secretario(self, secretario_id):
        # Cria uma nova janela para edição
        janela_edicao = ctk.CTkToplevel(self.root)
        janela_edicao.title("Editar Secretário")
        janela_edicao.geometry("700x400")
        janela_edicao.grab_set()
        # Centraliza a janela na tela
        largura_janela = 700
        altura_janela = 400
        largura_tela = janela_edicao.winfo_screenwidth()
        altura_tela = janela_edicao.winfo_screenheight()

        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2

        janela_edicao.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        # Cor de fundo da janela
        janela_edicao.configure(bg="#FAFAFA")

        # Obtém os dados atuais do secretário
        secretario_atual = get_secretario_por_id(self.conn, secretario_id)
        if not secretario_atual:
            messagebox.showerror("Erro", "Secretário não encontrado.")
            janela_edicao.destroy()
            return

        nome_atual, secretaria_atual = secretario_atual


        # Frame principal (campos de edição)
        frame_campos = ctk.CTkFrame(janela_edicao, fg_color="#FFFFFF", corner_radius=10)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=20)

        # Configurações de grid para layout responsivo
        for i in range(5):
            frame_campos.grid_columnconfigure(i, weight=1)
        frame_campos.grid_rowconfigure(0, weight=0)

        # Título
        label_titulo = ctk.CTkLabel(
            frame_campos,
            text="Edite o Secretário:",
            font=("Montserrat", 22, "bold"),
            text_color="#007E37"
        )
        label_titulo.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

            # --- Nome do Secretário ---
        label_nome = ctk.CTkLabel(
            frame_campos,
            text="Nome do Secretário:",
            font=("Montserrat", 14, "bold"),
            text_color="#007E37"
        )
        label_nome.grid(row=1, column=0, sticky="e", padx=10, pady=(5, 5))

        entrada_nome = ctk.CTkEntry(
            frame_campos,
            width=410,
            height=48,
            corner_radius=10,
            font=("Montserrat", 14),
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            text_color="#333333"
        )
        entrada_nome.insert(0, nome_atual)
        entrada_nome.grid(row=1, column=1, columnspan=3, sticky="ew", padx=10, pady=5)


        # --- Secretaria ---
        label_secretaria = ctk.CTkLabel(
            frame_campos,
            text="Secretaria:",
            font=("Montserrat", 14, "bold"),
            text_color="#007E37"
        )
        label_secretaria.grid(row=2, column=0, sticky="e", padx=10, pady=(5, 5))

        combo_secretarias = ctk.CTkComboBox(frame_campos,
                                        button_color="#019000",
                                        button_hover_color="#007E37",
                                        dropdown_fg_color="white",
                                        corner_radius=10,
                                        border_width=1,
                                        border_color="#CCCCCC",
                                        fg_color="white",
                                        font=("Montserrat", 14),
                                        dropdown_font=("Montserrat", 14),
                                        text_color_disabled="#333333",
                                        text_color="#333333",
                                        width=480,
                                        height=48,
                                        values=self.get_lista_secretarias())
        combo_secretarias.set(secretaria_atual)
        combo_secretarias.grid(row=2, column=1, columnspan=3, sticky="ew", padx=10, pady=5)

        def salvar_edicao():
            novo_nome = entrada_nome.get().strip()
            nova_secretaria = combo_secretarias.get().strip()
            if not novo_nome or not nova_secretaria:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return
            try:
                editar_secretario(self.conn, secretario_id, novo_nome, nova_secretaria)
                self.atualizar_lista_secretarios()
                messagebox.showinfo("Sucesso", "Dados do secretário atualizados com sucesso!")
                janela_edicao.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar secretário: {e}")

        ctk.CTkButton(janela_edicao, 
                            text="Salvar",
                            image=self.icons["editar"],  # Descomente esta linha caso tenha um ícone
                            fg_color="#019000",
                            text_color="#FFFFFF",
                            hover_color="#007E37",
                            compound="left",
                            width=155,
                            height=48,
                            font=("Montserrat", 16, "bold"),
                            command=salvar_edicao).pack(pady=20)


        def salvar_edicao():
            novo_nome = entrada_nome.get().strip()
            nova_secretaria = combo_secretarias.get().strip()
            if not novo_nome or not nova_secretaria:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return
            try:
                editar_secretario(self.conn, secretario_id, novo_nome, nova_secretaria)
                self.atualizar_lista_secretarios()
                messagebox.showinfo("Sucesso", "Dados do secretário atualizados com sucesso!")
                janela_edicao.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar secretário: {e}")


# Secretário fim

    def adicionar_ata_principal(self):
        descricao = self.descricao_ata.get()
        data = self.entrada_data_ata.get()
        horario_inicio = self.entrada_horario_inicio.get().strip()
        horario_termino = self.entrada_horario_termino.get().strip()
        
        if not descricao or not data or not horario_inicio or not horario_termino:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        if descricao and data and horario_inicio and horario_termino:
            adicionar_ata(self.conn, descricao, data, horario_inicio, horario_termino)
            self.descricao_ata.delete(0, ctk.END)
            self.entrada_horario_inicio.delete(0, ctk.END)
            self.entrada_horario_termino.delete(0, ctk.END)
            #self.atualizar_comboboxes()
            self.atualizar_lista_atas()
            messagebox.showinfo("Sucesso", "Ata adicionada!")


    def adicionar_fala(self):
        ata = self.combo_atas.get().split('-')[0].strip()  # Captura apenas a descrição da ata
        secretario = self.combo_secretarios.get().split(' (')[0].strip()  # Captura apenas o nome do secretário
        fala = self.html_editor_fala.html_editor.get("1.0", "end").strip()  # Captura o HTML do editor

        if ata and secretario and fala:
            try:
                adicionar_fala(self.conn, ata, secretario, fala)
                self.html_editor_fala.set_html("")  # Reseta o editor
                messagebox.showinfo("Sucesso", "Fala adicionada!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar fala: {e}")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def show_fala_popup(self, fala):
        popup = tk.Toplevel()
        popup.title("Texto Completo da Fala")
        popup.geometry("400x300")
        text_widget = tk.Text(popup, wrap="word", font=("Montserrat", 12))
        text_widget.insert("1.0", fala)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
        button_close = tk.Button(popup, text="Fechar", command=popup.destroy)
        button_close.pack()

    # Menu secretário Início
    def menu_secretario(self):
        self.clear_content_frame()
        # Frame para o cabeçalho
        main_container, header_frame = Containers.container_pages(self)

        # Botão de voltar
        Botoes.btn_voltar(self, header_frame)

        # ----------------------------------------------------------------
        # PRIMEIRO BLOCO EM BRANCO: “Criação de Secretario”
        # ----------------------------------------------------------------
        frame_secretario = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        frame_secretario.pack(fill="x", padx=400, pady=(20, 20))

        # ---------- Seção: Criação de Secretaria ----------
        section_secretario = ctk.CTkFrame(frame_secretario, fg_color="white")
        section_secretario.pack(fill="x", pady=(10, 10))

        label_secretario = ctk.CTkLabel(
            section_secretario,
            text="Adicionar Secretário",
            font=("Montserrat", 22, "bold"),
            text_color="#007E37"
        )
        label_secretario.pack(anchor="w", pady=(0, 5), padx=10)


        # Frame único para agrupar os campos em linha
        row_secretario = ctk.CTkFrame(section_secretario, fg_color="white")
        row_secretario.pack(fill="x")

        # Campo "Cadastro da Secretario"
        self.entrada_secretario  = ctk.CTkEntry(
            row_secretario, 
            placeholder_text="Nome da Secretario", 
            width=380,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            font=("Montserrat", 16)
        )
        self.entrada_secretario.pack(side="left", padx=15, pady=5)
    
        # Combo secretarias
        self.combo_secretarias = ctk.CTkComboBox(row_secretario,
                                                values=['Selecione uma Secretaria'],
                                                button_color="#019000",
                                                button_hover_color="#007E37",
                                                dropdown_fg_color="white",
                                                corner_radius=10,
                                                border_width=1,
                                                border_color="#CCCCCC",
                                                fg_color="white",
                                                font=("Montserrat", 14),
                                                dropdown_font=("Montserrat", 14),
                                                text_color_disabled="#333333",
                                                text_color="#333333",
                                                width=480,
                                                height=48)
        self.combo_secretarias.pack(side="left", padx=5, pady=5)
        # Botão "+ Nova Secretaria" (fica à extrema direita)
        botao_adicionar_secretario = ctk.CTkButton(
            row_secretario, 
            image=self.icons["adicionar"],
            text="Adicionar",
            fg_color="#019000",
            text_color="#FFFFFF",
            hover_color="#007E37",
            compound="left",
            width=155,
            height=48,
            font=("Montserrat", 16, "bold"),
            command=self.adicionar_secretario
        )
        botao_adicionar_secretario.pack(side="right", padx=10, pady=5)


        # ----------------------------------------------------------------
        # SEGUNDO BLOCO EM BRANCO: Listar Secretarios
        # ----------------------------------------------------------------

        card_secretarios = ctk.CTkFrame(main_container, 
                                        fg_color="white",
                                        corner_radius=10,
                                        )
        card_secretarios.pack(fill="x", padx=400, pady=(0, 10))

        # Frame para o label da lista (primeira linha)
        label_frame_secretarios = ctk.CTkFrame(card_secretarios, fg_color="white")
        label_frame_secretarios.pack(fill="x", pady=(10, 0), anchor="w")

        label_lista_secretarios = ctk.CTkLabel(label_frame_secretarios, 
                                        text="Secretários",
                                        font=("Montserrat", 22, "bold"),
                                        text_color="#007E37"  
                                        )
        label_lista_secretarios.pack(fill="none", anchor="w", padx=10, pady=(5, 10))
       
        # Atualiza o combobox com as secretarias disponíveis
        #self.atualizar_comboboxes()

        # Frame para listagem de Secretarios
        frame_lista_secretarios = ctk.CTkFrame(  
                                        card_secretarios, 
                                        bg_color="white",
                                        fg_color="white"
                                        )
        frame_lista_secretarios.pack(fill="both", expand=True, pady=(0, 20), padx=10)

        self.lista_secretarios = ctk.CTkScrollableFrame(
                                    frame_lista_secretarios, 
                                    width=800, 
                                    height=400, 
                                    fg_color="white",
                                    border_color="#FFFFFF", 
                                    border_width=2, 
                                    corner_radius=10,
                                    scrollbar_button_color="#CACACA",
                                    scrollbar_fg_color="white",
                                    scrollbar_button_hover_color="#007E37",
                                    bg_color="white",
                                    label_fg_color="white",
                                    label_text_color="#007E37",
                                    label_font=("Montserrat", 16, "bold"),
                                    
                                    )
        self.lista_secretarios.pack(fill="both", expand=True)

        # Footer
        Footer.footer_container(self, main_container, self.icons["logo_principal"])
        self.atualizar_lista_secretarios()

        # Menu secretario fim

        # Menu ata inicio
    def menu_atas(self):
            # Frame principal paginas
            main_container, header_frame = Containers.container_pages(self)

            # Botão de voltar
            Botoes.btn_voltar(self, header_frame)

            # Título do menu
            CriarAta.criar_ata(self, main_container)


            # ----------------------------------------------------------------
            # SEGUNDO BLOCO EM BRANCO: Listar Atas
            # ----------------------------------------------------------------

            card_atas = ctk.CTkFrame(main_container, 
                                            fg_color="white",
                                            corner_radius=10,
                                            )
            card_atas.pack(fill="x", padx=400, pady=(0, 10))

            # Frame para o label da lista (primeira linha)
            label_frame_atas = ctk.CTkFrame(card_atas, fg_color="white")
            label_frame_atas.pack(fill="x", pady=(10, 0), anchor="w")

            label_lista_atas = ctk.CTkLabel(label_frame_atas, 
                                            text="Atas",
                                            font=("Montserrat", 22, "bold"),
                                            text_color="#007E37"  
                                            )
            label_lista_atas.pack(fill="none", anchor="w", padx=10, pady=(5, 10))


           # Frame para listagem de Atas
            frame_lista_atas = ctk.CTkFrame(  
                                        card_atas, 
                                        bg_color="white",
                                        fg_color="white",  
     
            )
            frame_lista_atas.pack(fill="both", expand=True, pady=(0, 20), padx=10)

            self.lista_atas = ctk.CTkScrollableFrame(
                                    frame_lista_atas, 
                                    width=800, 
                                    height=400, 
                                    fg_color="white",
                                    border_color="#FFFFFF", 
                                    border_width=2, 
                                    corner_radius=10,
                                    scrollbar_button_color="#CACACA",
                                    scrollbar_fg_color="white",
                                    scrollbar_button_hover_color="#007E37",
                                    bg_color="white",
                                    label_fg_color="white",
                                    label_text_color="#007E37",
                                    label_font=("Montserrat", 20, "bold"),
                                    
                                    )
        
            self.lista_atas.pack(fill="both", expand=True)

            #self.atualizar_comboboxes()
            self.atualizar_lista_atas()

            # Footer
            Footer.footer_container(self, main_container, self.icons["logo_principal"])


    def atualizar_lista_atas(self):
        for widget in self.lista_atas.winfo_children():
            widget.destroy()

        atas = listar_atas(self.conn)

        for ata in atas:
            frame = ctk.CTkFrame(self.lista_atas, bg_color="white", fg_color="white" )
            frame.pack(fill="x", padx=5, pady=5)

            descricao = f"{ata[1]} ({ata[2]})"
            ctk.CTkLabel(frame, text=descricao, 
                         font=("Montserrat", 16), 
                         text_color="#333333").pack(side="left", padx=5)


            botao_deletar = ctk.CTkButton(frame,                                          
                                          fg_color="#E7000B", 
                                          image=self.icons["deletar"], 
                                          text="Deletar", 
                                          hover_color="#B7070F", 
                                          text_color="#FFFFFF",
                                          font=("Montserrat", 16, "bold"),
                                          command=lambda a_id=ata[0]: self.deletar_ata(a_id), 
                                          )
            botao_deletar.pack(side="right", padx=5)

            botao_editar = ctk.CTkButton(frame, 
                                         fg_color="#00AAA7", 
                                         image=self.icons["editar"], 
                                         text="Editar", 
                                         hover_color="#009693", 
                                         text_color="#FFFFFF",
                                         font=("Montserrat", 16, "bold"),
                                         command=lambda a_id=ata[0]: self.editar_ata(a_id), 
                                         )
            botao_editar.pack(side="right", padx=5)

            botao_exportar = ctk.CTkButton(frame, 
                                         text="Exportar",                      
                                         fg_color="#FFA500", 
                                         image=self.icons["exportar"], 
                                         hover_color="#E49400", 
                                         text_color="#FFFFFF",
                                         font=("Montserrat", 16, "bold"),
                                         command=lambda a_id=ata[0]: self.exportar_ata_ui(a_id), 
                                         )
            botao_exportar.pack(side="right", padx=5)

    def exportar_ata_ui(self, ata_id):
        try:
            descricao, data, falas, horario_inicio, horario_termino = obter_dados_ata(self.conn, ata_id)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return

        pasta_destino = filedialog.askdirectory(title="Selecione a pasta para salvar o PDF")
        if not pasta_destino:
            return

        filename = os.path.join(pasta_destino, f"ata_{descricao}.pdf")

        # Agrupa as falas por secretário.
        secretarios_dict = {}
        for fala in falas:
            _, secretario, fala_texto = fala
            if secretario not in secretarios_dict:
                secretarios_dict[secretario] = []
            secretarios_dict[secretario].append(fala_texto)

        # Ordena os secretários em ordem alfabética.
        secretarios_ordenados = sorted(secretarios_dict.items(), key=lambda x: x[0])

        # Cria strings para mostrar na tabela
        # 1) Lista de secretários (um por linha, ou separados por vírgula)
        lista_secretarios_str = "<br/>".join([sec[0] for sec in secretarios_ordenados])

        # 2) Lista das falas (secretário + fala). Aqui, faremos um HTML básico
        #    para que cada fala quebre a linha.
        falas_str = ""
        for secretario, falas_list in secretarios_ordenados:
            for fala_texto in falas_list:
                falas_str += f"<b>{secretario}:</b> {fala_texto}<br/>"
        
        # Ajuste o caminho da imagem e o tamanho (largura x altura).
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "assets", "img", "logo.png")
        logo_largura = 176
        logo_altura = 46

        # Vamos usar o SimpleDocTemplate, que aceita uma lista de “flowables” (Elementos).
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        
        # Crie um objeto Image para a logo
        logo_img = Image(logo_path, width=logo_largura, height=logo_altura)
        
        # Parágrafos formatados para o título, subtítulos etc.
        titulo_texto = f"<b>{descricao} - {data} - {horario_inicio} às {horario_termino}</b>"
        titulo_paragrafo = Paragraph(titulo_texto, styles["Title"])  
        
        secretarios_title = Paragraph("<b>Secretários participantes:</b>", styles["Normal"])
        secretarios_paragrafo = Paragraph(lista_secretarios_str, styles["Normal"])

        falas_title = Paragraph("<b>Falas:</b>", styles["Normal"])
        falas_paragrafo = Paragraph(falas_str, styles["Normal"])

        # Agora montamos uma tabela com 3 linhas e 2 colunas:
        #   [ [LOGO, TITULO],
        #     [Secretários participantes, lista de secretários],
        #     [Falas, falas em geral] ]
        data_table = [
            [logo_img, titulo_paragrafo],
            [secretarios_title, secretarios_paragrafo],
            [falas_title,       falas_paragrafo]
        ]

        # Ajuste as larguras de cada coluna (colWidths). Aqui, a 1ª coluna terá 200pt e a 2ª terá 300pt.
        # Ajuste conforme seu layout desejado.
        table = Table(data_table, colWidths=[200, 300])
        
        # Definimos um estilo para alinhar o topo de cada célula, cor de fundo etc. (opcional).
        # Exemplo: deixamos tudo alinhado no topo e inserimos algum espaçamento interno (padding).
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('VALIGN', (0,0), (0,0), 'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX',       (0,0), (-1,-1), 0.25, colors.black),
            ('LEFTPADDING',(0,0),(-1,-1), 10),
            ('RIGHTPADDING',(0,0),(-1,-1), 10),
            ('TOPPADDING',(0,0),(-1,-1), 5),
            ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ]))

        # Montamos a “story” (lista de flowables) e adicionamos a tabela.
        story = []
        story.append(table)
        story.append(Spacer(1, 12))  # Espaço em branco se desejar

        # Finalmente, construímos o PDF
        doc.build(story)

        messagebox.showinfo("Sucesso", f"PDF exportado com sucesso:\n{filename}")


    def editar_ata(self, ata_id):
        janela_edicao = ctk.CTkToplevel(self.root)
        janela_edicao.title("Editar Ata")
        janela_edicao.geometry("650x400")
        
        # Aguarda a janela estar visível antes de calcular a posição correta
        janela_edicao.grab_set()

        largura_janela = 650
        altura_janela = 400
        largura_tela = janela_edicao.winfo_screenwidth()
        altura_tela = janela_edicao.winfo_screenheight()

        # Calcula as coordenadas para centralizar a janela
        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2

        # Aplica a nova posição centralizada
        janela_edicao.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        # Aplica as cores padrão
        janela_edicao.configure(bg="#FAFAFA")    

        
        ata_atual = [ata for ata in listar_atas(self.conn) if ata[0] == ata_id]
        if not ata_atual:
            messagebox.showerror("Erro", "Ata não encontrada.")
            janela_edicao.destroy()
            return


        descricao_atual, data_atual, horario_inicio, horario_fim = ata_atual[0][1], ata_atual[0][2], ata_atual[0][3], ata_atual[0][4]

        # Frame principal que conterá os campos de edição
        frame_campos = ctk.CTkFrame(janela_edicao, fg_color="#FFFFFF", corner_radius=10)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=20)

        # Configurando linhas e colunas do grid para melhor disposição
        for i in range(5):  # Ajuste conforme o número total de colunas
            frame_campos.grid_columnconfigure(i, weight=1)

        frame_campos.grid_rowconfigure(0, weight=0)  # Impede expansão do título

        # Label alinhado à esquerda
        label = ctk.CTkLabel(frame_campos, text="Edite a ata:", 
                            font=("Montserrat", 22, "bold"), 
                            text_color="#007E37")
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")



        # --- Descrição da Ata ---
        label_descricao = ctk.CTkLabel(frame_campos, text="Nome da Ata:",font=("Montserrat", 14, "bold"), text_color="#007E37")
        label_descricao.grid(row=1, column=0, sticky="e", padx=10, pady=(5, 5)) 

        entrada_descricao = ctk.CTkEntry(frame_campos,      
                                            width=410,
                                            height=48,
                                            corner_radius=10,
                                            font=("Montserrat", 14),
                                            border_width=1,
                                            border_color="#CCCCCC",
                                            fg_color="white",
                                            text_color="#333333")
        entrada_descricao.insert(0, descricao_atual)
        entrada_descricao.grid(row=1, column=1, columnspan=3, sticky="ew", padx=10, pady=5)

        # --- Data da Ata ---
        label_data = ctk.CTkLabel(frame_campos, text="Data da Ata:", font=("Montserrat", 14, "bold"), text_color="#007E37")
        label_data.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        entrada_data = CustomDatePicker(
            frame_campos, 
            width=140, 
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white"
        )

        entrada_data.set_date(data_atual)
        entrada_data.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # --- Horário de Início e Horário de Término na mesma linha ---
        label_horario_inicio = ctk.CTkLabel(frame_campos, text="Horário de Início:"          
                                           ,font=("Montserrat", 14, "bold"), text_color="#007E37")
        label_horario_inicio.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        entrada_horario_inicio = ctk.CTkEntry(frame_campos,
                                            placeholder_text="HH:MM",
                                            width=70,
                                            height=48,
                                            corner_radius=10,
                                            font=("Montserrat", 14),
                                            border_width=1,
                                            border_color="#CCCCCC",
                                            fg_color="white",
                                            text_color="#333333")
        entrada_horario_inicio.insert(0, horario_inicio)
        entrada_horario_inicio.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        label_horario_termino = ctk.CTkLabel(frame_campos, 
                                                        text="Horário de Término:",font=("Montserrat", 14, "bold"), text_color="#007E37")
        label_horario_termino.grid(row=3, column=2, sticky="e", padx=10, pady=5)

        entrada_horario_termino = ctk.CTkEntry(frame_campos,                                       
                                            placeholder_text="HH:MM",
                                            width=70,
                                            height=48,
                                            corner_radius=10,
                                            font=("Montserrat", 14),
                                            border_width=1,
                                            border_color="#CCCCCC",
                                            fg_color="white",
                                            text_color="#333333")
        entrada_horario_termino.insert(0, horario_fim)
        entrada_horario_termino.grid(row=3, column=3, sticky="w", padx=10, pady=5)

        def salvar_edicao():
            nova_descricao = entrada_descricao.get().strip()
            nova_data = entrada_data.get().strip()
            novo_horario_inicio = entrada_horario_inicio.get().strip()
            novo_horario_termino = entrada_horario_termino.get().strip()
            if not nova_descricao or not nova_data:
                messagebox.showerror("Erro", "A descrição e a data não podem estar vazias.")
                return
            try:
                editar_ata(self.conn, ata_id, nova_descricao, nova_data, novo_horario_inicio, novo_horario_termino)
                self.atualizar_lista_atas()
                messagebox.showinfo("Sucesso", "Ata atualizada com sucesso!")
                janela_edicao.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar ata: {e}")

        ctk.CTkButton(janela_edicao, 
                                text="Salvar", 
                                image=self.icons["editar"],
                                fg_color="#019000",
                                text_color="#FFFFFF",
                                hover_color="#007E37",
                                compound="left",
                                width=155,
                                height=48,
                                font=("Montserrat", 16, "bold"),
                                command=salvar_edicao).pack(pady=15, side="right", expand=True, padx=25)

    def deletar_ata(self, ata_id):
        resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja deletar esta ata?")
        if resposta:
            try:
                deletar_ata(self.conn, ata_id)
                self.atualizar_lista_atas()
                messagebox.showinfo("Sucesso", "Ata deletada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar ata: {e}")

        # Menu ata fim
 


    def listar_atas(self):

        # Frame principal paginas
        main_container, header_frame = Containers.container_pages(self)

        # Botão de voltar
        Botoes.btn_voltar(self, header_frame)

        # ----------------------------------------------------------------
        # PRIMEIRO BLOCO EM BRANCO: “Buscar de Ata”
        # ----------------------------------------------------------------
        card_buscar = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        card_buscar.pack(fill="x", padx=400, pady=(20, 20))

        # ---------- Seção: Busca ----------
        frame_busca = ctk.CTkFrame(card_buscar, fg_color="white")
        frame_busca.pack(fill="x", pady=(10, 10), anchor="w")  # Alinha todo o frame à esquerda
        
        label_busca = ctk.CTkLabel(frame_busca, 
                        text="Buscar fala",
                        font=("Montserrat", 22, "bold"),
                        text_color="#007E37"                               ,
        )
        label_busca.pack(fill="none", anchor="w", padx=5, pady=(5, 10))

        # Frame para campo e botão na segunda linha
        input_frame = ctk.CTkFrame(frame_busca, fg_color="white")
        input_frame.pack(fill="x", expand=True)

        campo_busca = ctk.CTkEntry(input_frame,            
                            placeholder_text="Busca", 
                            width=280,
                            height=48,
                            corner_radius=10,
                            border_width=1,
                            border_color="#CCCCCC",
                            fg_color="white",
                            font=("Montserrat", 16)
        )
        campo_busca.pack(side="left", fill="x", expand=True, padx=15, pady=10)

        botao_busca = ctk.CTkButton(input_frame, 
                        text="Pesquisar", 
                        image=self.icons["pesquisar"],
                        fg_color="#019000",
                        text_color="#FFFFFF",
                        hover_color="#007E37",
                        compound="left",
                        width=155,
                        height=48,
                        font=("Montserrat", 16, "bold"),
                        command=lambda: atualizar_lista(campo_busca.get()))
        botao_busca.pack(side="left", padx=5, pady=5)

        # ----------------------------------------------------------------
        # SEGUNDO BLOCO EM BRANCO: Listar falas das Atas”
        # ----------------------------------------------------------------
        
        card_fala_atas = ctk.CTkFrame(main_container, fg_color="white",  corner_radius=10)
        card_fala_atas.pack(fill="x", padx=400, pady=(0, 10))

        # Frame para o label da lista (primeira linha)
        label_frame = ctk.CTkFrame(card_fala_atas, fg_color="white")
        label_frame.pack(fill="x", pady=(10, 0), anchor="w")

        label_lista_atas = ctk.CTkLabel(label_frame, 
                                        text="Lista de Atas",
                                        font=("Montserrat", 22, "bold"),
                                        text_color="#007E37"  
                                        )
        label_lista_atas.pack(fill="none", anchor="w", padx=10, pady=(5, 10))

        # Frame para a lista e scrollbar (segunda linha)
        frame_lista_atas = ctk.CTkFrame(
                                        card_fala_atas, 
                                        fg_color="white",          # Background color
                                        border_width=0,        # Remove a borda preta
                                        corner_radius=10       # Mantém as bordas arredondadas


        )
        frame_lista_atas.pack(fill="both", expand=True, pady=(0, 20), padx=10)
       
        # Criar o Treeview
        lista_atas = ttk.Treeview(frame_lista_atas, style="Treeview", columns=("Secretário", "Fala"), show="tree headings", height=10)

        # Configurar o tamanho da fonte
        style = ttk.Style()
        style.configure("Treeview", font=("Montserrat", 14), borderwidth=0, relief="flat")  # Remover qualquer contorno
        style.configure("Treeview.Heading", font=("Montserrat", 14), borderwidth=0, relief="flat")  # Remover borda dos cabeçalhos
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remover padding interno que cria borda visual

        # Definir o cabeçalho
        lista_atas.heading("#0", text="Ata (Descrição - Data)")
        lista_atas.heading("Secretário", text="Secretário / Secretaria")
        lista_atas.heading("Fala", text="Fala")
        lista_atas.column("Secretário", width=200)
        lista_atas.column("Fala", width=400)
        
        # Definir largura das colunas para garantir que o scroll horizontal tenha efeito
        lista_atas.column("#0", width=600, stretch=True)
        lista_atas.column("Secretário", width=350, stretch=True)
        lista_atas.column("Fala", width=600, stretch=True)

        # Criar e configurar Scrollbars
        scrollbar_vertical = ttk.Scrollbar(frame_lista_atas, orient="vertical", command=lista_atas.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame_lista_atas, orient="horizontal", command=lista_atas.xview)
        lista_atas.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

        
        # Posicionar os componentes na tela
        lista_atas.pack(side="top", fill="both", expand=True)
        scrollbar_vertical.pack(side="right", fill="y")
        scrollbar_horizontal.pack(side="bottom", fill="x")

        # Footer
        Footer.footer_container(self, main_container, self.icons["logo_principal"])

        # Função para atualizar a lista de atas
        def atualizar_lista(filtro):
            # Limpar o Treeview
            for item in lista_atas.get_children():
                lista_atas.delete(item)

            # Obter atas (todas ou filtradas)
            if filtro.strip():
                atas = buscar_atas_por_descricao(self.conn, filtro)
            else:
                atas = listar_atas(self.conn)

            # Vamos criar um dicionário: { "desc completa": [(fala_id, secretário, fala_texto), ...], ... }
            dados_atas = {}
            for ata in atas:
                numero_ata = ata[0]
                descricao_ata = ata[1]
                data_ata = ata[2]
                descricao_completa = f"{descricao_ata} - {data_ata}"

                # Se ainda não existe no dicionário, inicializa
                dados_atas[descricao_completa] = []

                # Obter falas vinculadas à ata
                falas = listar_falas_por_ata(self.conn, numero_ata)
                for fala in falas:
                    fala_id = fala[0]            # ID da fala no BD
                    secretario_nome = fala[1]   # Nome do secretário
                    fala_texto = fala[2]        # Texto da fala

                    secretaria_nome = get_secretaria_by_secretario(self.conn, secretario_nome)
                    secretario_completo = f"{secretario_nome} ({secretaria_nome})"
                    
                    dados_atas[descricao_completa].append((fala_id, secretario_completo, fala_texto))

            # Inserir dados no Treeview
            for descricao_completa, lista_falas in dados_atas.items():
                # Cria o item "pai" para a ata
                item_ata = lista_atas.insert("", "end", text=descricao_completa)
                
                # Para cada fala, vamos inserir um item filho.
                # Aqui, vamos armazenar o fala_id no "text" e os valores (secretário, fala) em "values"
                for fala_id, secretario_completo, fala_texto in lista_falas:
                    lista_atas.insert(item_ata, "end",
                                      text=f"{fala_id}",
                                      values=(secretario_completo, fala_texto))

        # Inicializar a lista de atas
        atualizar_lista("")

        # Função para capturar a fala selecionada e mostrar no popup
        def on_double_click(event):
            selected_item = lista_atas.selection()
            if selected_item:
                # Pegamos o item clicado
                fala_id_str = lista_atas.item(selected_item[0], "text")     # text é onde guardamos o ID
                fala_data = lista_atas.item(selected_item[0], "values")     # values é (secretario, fala)
                
                if fala_data and len(fala_data) == 2:
                    # Convertendo fala_id_str para inteiro, se necessário
                    # (desde que fala_id_str não seja vazio)
                    fala_id = None
                    if fala_id_str.isdigit():
                        fala_id = int(fala_id_str)
                    
                    # O texto da fala fica no segundo índice (0=secretário, 1=fala)
                    texto_atual = fala_data[1]
                    
                    # Exibe o popup de edição. Agora temos fala_id e texto.
                    self.show_fala_popup(fala_id, texto_atual)

        # Associar o evento de clique duplo ao Treeview
        lista_atas.bind("<Double-1>", on_double_click)

    # fim listar_atas

    def show_fala_popup(self, fala_id, texto_atual):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Fala")
        popup.geometry("600x400")
        
        # Centralizar na tela
        popup.update_idletasks()
        largura_janela = 600
        altura_janela = 400
        largura_tela = popup.winfo_screenwidth()
        altura_tela = popup.winfo_screenheight()
        x = (largura_tela - largura_janela) // 2
        y = (altura_tela - altura_janela) // 2
        popup.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        # Cor de fundo e estrutura
        popup.configure(bg="#FAFAFA")

        # Frame principal
        container = ctk.CTkFrame(popup, fg_color="#FFFFFF", corner_radius=10)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Título do pop-up
        label = ctk.CTkLabel(container, text="Edite a fala:", text_color="#019000",  font=("Montserrat", 22, "bold"))
        label.pack(pady=10)

        # Campo de texto
        texto_fala = ctk.CTkTextbox(container, wrap="word",  font=("Montserrat", 16), height=6, corner_radius=5)
        texto_fala.insert("1.0", texto_atual)
        texto_fala.pack(fill="both", expand=True, padx=10, pady=10)

        # Botão para salvar a edição
        def salvar_fala():
            novo_texto = texto_fala.get("1.0", "end").strip()
            if fala_id is None:
                # Se não tivermos o ID, não podemos atualizar no BD
                self.show_error_message("Não há ID para atualizar a fala.")
                return

            try:
                # Atualiza o banco de dados com o novo texto da fala
                atualizar_fala(self.conn, fala_id, novo_texto)
            
                # Fecha o pop-up após salvar
                popup.destroy()
                
                # Atualiza a lista de atas no Treeview para refletir as mudanças
                self.listar_atas()
                # Exibe uma mensagem de sucesso
                messagebox.showinfo("Sucesso", "Fala atualizada com sucesso!")

            except Exception as e:
                # Exibe uma mensagem de erro caso algo dê errado
                messagebox.showerror("Erro", f"Erro ao atualizar fala: {e}")

        # Botão para deletar a fala
        def deletar_fala_popup():
            if fala_id is None:
                self.show_error_message("Não há ID para deletar a fala.")
                return

            try:
                # Confirmação de exclusão
                if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar esta fala?"):
                    deletar_fala(self.conn, fala_id)  # Chama a função para deletar no banco
                    popup.destroy()
                    self.listar_atas()  # Atualiza a lista de atas
            except Exception as e:
                self.show_error_message(f"Erro ao deletar fala: {e}")
        # Botões de ação
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        # Botão para salvar
        botao_salvar = ctk.CTkButton(button_frame, text="Salvar", 
                                    image=self.icons["editar"],
                                    fg_color="#019000",
                                    text_color="#FFFFFF",
                                    hover_color="#007E37",
                                    compound="left",
                                    width=155,
                                    height=48,
                                    font=("Montserrat", 16, "bold"),
                                    command=salvar_fala)
        botao_salvar.pack(side="right", expand=True, padx=5)


        # Botão para deletar
        botao_deletar = ctk.CTkButton(button_frame, text="Deletar",        
                                        fg_color="#E7000B", 
                                        image=self.icons["deletar"], 
                                        hover_color="#B7070F", 
                                        text_color="#FFFFFF",
                                        width=155,
                                        height=48,
                                        font=("Montserrat", 16, "bold"),
                                        command=deletar_fala_popup
        )
        botao_deletar.pack(side="left", expand=True, padx=5)
        popup.grab_set()  # Impede interações na janela principal enquanto o pop-up está aberto


    # Função para limpar todas as atas e falas
    def limpar_todas_as_entidades(self):
        resultado = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar TODAS as atas e falas?")
        if resultado:
            cursor = self.conn.cursor()
    
            # Deleta todas as falas
            cursor.execute("DELETE FROM falas")

            # Deleta todas as atas
            cursor.execute("DELETE FROM atas")
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Todas as atas e falas foram deletadas.")
            # Chamar a função para atualizar a view
            self.listar_atas()




# Função principal
if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    conn.close()

    root = ctk.CTk()
    app = MeetingManagerApp(root)
    root.mainloop()
