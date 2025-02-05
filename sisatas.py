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
from utils.images import load_icons
from utils.CustomDatePicker import CustomDatePicker
from utils.CTkHTMLScrolledText import CTkHTMLScrolledText


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
        header_frame.pack(fill="x", pady=(20, 10))


    # ---------- Título ----------
        label_titulo = ctk.CTkLabel(
            header_frame,
            text="Gerenciador de Atas",
            text_color="#019000",
            font=("Arial", 36, "bold")
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
            width=156,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Arial", 16),
            command=self.listar_atas
        )
        botao_buscar.grid(row=0, column=1, padx=5, pady=10)  # sem sticky="ew" para manter a largura fixa

        # Botão de Carregar Menu da Atas
        botao_listar_atas = ctk.CTkButton(
            container_botoes, 
            text="Lista de atas",
            image=self.icons["atas"],
            compound="left",
            width=156,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Arial", 16),
            command=self.menu_atas  # Exemplo de callback
        )
        botao_listar_atas.grid(row=0, column=2, padx=5, pady=10)

        # Botão de Carregar Menu da Secretaria
        botao_secretarias = ctk.CTkButton(
            container_botoes, 
            text="Secretarias",
            image=self.icons["secretarias"],
            compound="left",
            width=156,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Arial", 16),
            command=self.menu_secretaria  # Exemplo de callback
        )
        botao_secretarias.grid(row=0, column=3, padx=5, pady=10)

        # Botão de Carregar Menu da Secretarios
        botao_secretarios = ctk.CTkButton(
            container_botoes,
            text="Secretários",
            image=self.icons["secretarios"],
            compound="left",
            width=156,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            font=("Arial", 16),
            command=self.menu_secretario  # Exemplo de callback
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
            font=("Arial", 16),
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
            font=("Arial", 16),
            command=self.realizar_backup  # callback
        )
        botao_exportar.grid(row=0, column=6, padx=5, pady=10)

        # ----------------------------------------------------------------
        # PRIMEIRO BLOCO EM BRANCO: “Criação de Ata”
        # ----------------------------------------------------------------
        card_ata = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        card_ata.pack(fill="x", padx=40, pady=(20, 20))

        # ---------- Seção: Criação de Ata ----------
        section_ata = ctk.CTkFrame(card_ata, fg_color="white")
        section_ata.pack(fill="x", padx=20, pady=(10, 10))

        label_ata = ctk.CTkLabel(
            section_ata,
            text="Criação de Ata",
            font=("Arial", 22, "bold"),
            text_color="#007E37"
        )
        label_ata.pack(anchor="w", pady=(0, 5))

        # Frame único para agrupar os campos em linha
        row_ata = ctk.CTkFrame(section_ata, fg_color="white")
        row_ata.pack(fill="x")

        # Campo "Nome da Ata"
        self.descricao_ata = ctk.CTkEntry(
            row_ata, 
            placeholder_text="Nome da Ata", 
            width=420,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            font=("Arial", 16)
        )
        self.descricao_ata.pack(side="left", padx=5, pady=5)

        # Campo de data (DatePicker customizado)
        # -> Não crie outro root, use simplesmente 'row_ata' como parent
        self.entrada_data_ata = CustomDatePicker(
            row_ata, 
            width=150, 
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white"
        )
        self.entrada_data_ata.pack(side="left", padx=10, pady=5)

        # Label "Horário de Início"
        label_inicio = ctk.CTkLabel(
            row_ata, 
            text="Horário de Início:", 
            font=("Arial", 12, "bold"),
            text_color="#007E37"
        )
        label_inicio.pack(side="left", padx=(20,5), pady=5)

        # Campo "Horário de Início"
        self.entrada_horario_inicio = ctk.CTkEntry(
            row_ata,
            placeholder_text="HH:MM",
            width=80,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            text_color="#333333"
        )
        self.entrada_horario_inicio.pack(side="left", padx=5, pady=5)

        # Label "Horário de Término"
        label_termino = ctk.CTkLabel(
            row_ata, 
            text="Horário de Término:",
            font=("Arial", 12, "bold"),
            text_color="#007E37"
        )
        label_termino.pack(side="left", padx=(20,5), pady=5)

        # Campo "Horário de Término"
        self.entrada_horario_termino = ctk.CTkEntry(
            row_ata,
            placeholder_text="HH:MM",
            width=80,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            text_color="#333333"
        )
        self.entrada_horario_termino.pack(side="left", padx=5, pady=5)

        # Botão "+ Nova Ata" (fica à extrema direita)
        botao_nova_ata = ctk.CTkButton(
            row_ata, 
            image=self.icons["adicionar"],
            text="Nova Ata",
            fg_color="#019000",
            text_color="#FFFFFF",
            hover_color="#007E37",
            compound="left",
            width=155,
            height=48,
            font=("Arial", 16),
            command=self.adicionar_ata_principal
        )
        botao_nova_ata.pack(side="right", padx=5, pady=5)

        # ----------------------------------------------------------------
        # SEGUNDO BLOCO EM BRANCO: “Criação de fala”
        # ----------------------------------------------------------------
        card_fala = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        card_fala.pack(fill="x", padx=40, pady=(0, 10))

        frame_fala = ctk.CTkFrame(card_fala, fg_color="white")
        frame_fala.pack(fill="x", padx=20, pady=(20, 20))

        label_fala = ctk.CTkLabel(
            frame_fala,
            text="Criação de fala",
            font=("Arial", 22, "bold"),
            text_color="#007E37"
        )
        label_fala.pack(anchor="w", pady=(0, 5))

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
            width=480,
            height=48
        )
        self.combo_atas.pack(side="left", padx=5, pady=5)

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
            text_color_disabled="#333333",
            text_color="#333333",
            width=520,
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
            width=80,
            height=10
        )
        self.html_editor_fala.pack(fill="x", padx=5, expand=True)

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
            font=("Arial", 16),
            command=self.adicionar_fala
        )
        botao_adicionar_fala.pack(side="right", pady=(10, 5))
        
        #self.geometry("800x200")

        # ----------------------------------------------------------------
        # LOGO NO RODAPÉ (pode ficar ao final, fora dos “cards”)
        # ----------------------------------------------------------------
        footer_frame = ctk.CTkFrame(main_container, fg_color="#FAFAFA")
        footer_frame.pack(fill="x", pady=(30, 10))

        label_logo = ctk.CTkLabel(footer_frame, text="", image=self.icons["logo_principal"], compound="top")
        label_logo.pack()

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

    def atualizar_lista_secretarias(self):
        for widget in self.lista_secretarias.winfo_children():
            widget.destroy()

        secretarias = listar_secretarias(self.conn)

        for secretaria in secretarias:
            frame = ctk.CTkFrame(self.lista_secretarias)
            frame.pack(fill="x", padx=5, pady=5)

            nome = f"{secretaria[1]}"

            ctk.CTkLabel(frame, text=nome).pack(side="left", padx=5)

            botao_editar = ctk.CTkButton(frame, text="Editar", command=lambda s_id=secretaria[0]: self.editar_secretaria(s_id), fg_color="#007bff", hover_color="#0056b3", text_color="#FFFFFF")
            botao_editar.pack(side="right", padx=5)

            botao_deletar = ctk.CTkButton(frame, text="Deletar", command=lambda s_id=secretaria[0]: self.deletar_secretaria(s_id), fg_color="#dc3545", hover_color="#b02a37", text_color="#FFFFFF")
            botao_deletar.pack(side="right", padx=5)


    def menu_secretaria(self):
        self.clear_content_frame()

        # Botão de voltar
        botao_voltar = ctk.CTkButton(self.root, text="Voltar", command=self.return_to_main_menu)
        botao_voltar.pack(anchor="nw", padx=10, pady=10)

        # Título do menu
        ctk.CTkLabel(self.root, text="Adicionar Secretaria", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame para cadastro de Secretaria
        frame_secretaria = ctk.CTkFrame(self.root)
        frame_secretaria.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_secretaria, text="Nome da Secretaria:").pack(side="left", padx=5, pady=5)

        self.entrada_secretaria = ctk.CTkEntry(frame_secretaria, placeholder_text="Digite o nome", width=300)
        self.entrada_secretaria.pack(side="left", padx=5, pady=5)

        botao_adicionar_secretaria = ctk.CTkButton(frame_secretaria, text="Adicionar", command=self.adicionar_secretaria, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF")
        botao_adicionar_secretaria.pack(side="left", padx=5, pady=5)

        # Título da listagem de secretarias
        ctk.CTkLabel(self.root, text="Secretarias", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame para listagem de Secretarias
        frame_lista_secretarias = ctk.CTkFrame(self.root)
        frame_lista_secretarias.pack(fill="both", expand=True, padx=10, pady=5)

        self.lista_secretarias = ctk.CTkScrollableFrame(frame_lista_secretarias, width=400, height=200)
        self.lista_secretarias.pack(fill="both", expand=True)

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
            frame = ctk.CTkFrame(self.lista_secretarias)
            frame.pack(fill="x", padx=5, pady=5)

            nome = f"{secretaria[1]}"

            ctk.CTkLabel(frame, text=nome).pack(side="left", padx=5)

            botao_deletar = ctk.CTkButton(frame, text="Deletar", command=lambda s_id=secretaria[0]: self.deletar_secretaria(s_id), fg_color="#dc3545", hover_color="#b02a37", text_color="#FFFFFF")
            botao_deletar.pack(side="right", padx=5)

            botao_editar = ctk.CTkButton(frame, text="Editar", command=lambda s_id=secretaria[0]: self.editar_secretaria(s_id), fg_color="#007bff", hover_color="#0056b3", text_color="#FFFFFF")
            botao_editar.pack(side="right", padx=5)

    def editar_secretaria(self, secretaria_id):
        # Cria uma nova janela para edição
        janela_edicao = ctk.CTkToplevel(self.root)
        janela_edicao.title("Editar Secretaria")
        janela_edicao.geometry("400x200")
        janela_edicao.grab_set()

        # Obtém o nome atual da secretaria do controller
        secretaria_atual = get_secretaria_por_id(self.conn, secretaria_id)

        if not secretaria_atual:
            messagebox.showerror("Erro", "Secretaria não encontrada.")
            janela_edicao.destroy()
            return

        nome_atual = secretaria_atual["nome"]

        ctk.CTkLabel(janela_edicao, text="Nome da Secretaria:").pack(pady=10)
        entrada_nome = ctk.CTkEntry(janela_edicao, width=300)
        entrada_nome.insert(0, nome_atual)
        entrada_nome.pack(pady=10)

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

        ctk.CTkButton(janela_edicao, text="Salvar", command=salvar_edicao, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF").pack(pady=20)

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
            frame = ctk.CTkFrame(self.lista_secretarios)
            frame.pack(fill="x", padx=5, pady=5)

            nome = f"{secretario[1]} ({secretario[2]})"
            status = "Ativo" if secretario[3] == 1 else "Inativo"

            ctk.CTkLabel(frame, text=nome).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=status).pack(side="left", padx=5)

            botao_editar = ctk.CTkButton(frame, text="Editar", command=lambda s_id=secretario[0]: self.editar_secretario(s_id), fg_color="#007bff", hover_color="#0056b3", text_color="#FFFFFF")
            botao_editar.pack(side="right", padx=5)

            if secretario[3] == 1:
                botao = ctk.CTkButton(frame, text="Desativar", command=lambda s_id=secretario[0]: self.desativar_secretario(s_id), fg_color="#ffa500", hover_color="#cc8400", text_color="#FFFFFF")
            else:
                botao = ctk.CTkButton(frame, text="Ativar", command=lambda s_id=secretario[0]: self.ativar_secretario(s_id), fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF")

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
        janela_edicao.geometry("400x300")
        janela_edicao.grab_set()

        # Obtém os dados atuais do secretário
        secretario_atual = get_secretario_por_id(self.conn, secretario_id)
        if not secretario_atual:
            messagebox.showerror("Erro", "Secretário não encontrado.")
            janela_edicao.destroy()
            return

        nome_atual, secretaria_atual = secretario_atual

        ctk.CTkLabel(janela_edicao, text="Nome do Secretário:").pack(pady=10)
        entrada_nome = ctk.CTkEntry(janela_edicao, width=300)
        entrada_nome.insert(0, nome_atual)
        entrada_nome.pack(pady=10)

        ctk.CTkLabel(janela_edicao, text="Secretaria:").pack(pady=10)
        combo_secretarias = ctk.CTkComboBox(janela_edicao, values=self.get_lista_secretarias(), width=300)
        combo_secretarias.set(secretaria_atual)
        combo_secretarias.pack(pady=10)

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

        ctk.CTkButton(janela_edicao, text="Salvar", command=salvar_edicao, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF").pack(pady=20)


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

        ctk.CTkButton(janela_edicao, text="Salvar", command=salvar_edicao, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF").pack(pady=20)

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
            self.atualizar_comboboxes()
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
        text_widget = tk.Text(popup, wrap="word", font=("Arial", 12))
        text_widget.insert("1.0", fala)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
        button_close = tk.Button(popup, text="Fechar", command=popup.destroy)
        button_close.pack()

    # Menu secretário Início
    def menu_secretario(self):
        self.clear_content_frame()

        # Botão de voltar
        botao_voltar = ctk.CTkButton(self.root, text="Voltar", command=self.return_to_main_menu)
        botao_voltar.pack(anchor="nw", padx=10, pady=10)

        # Título do menu
        ctk.CTkLabel(self.root, text="Adicionar Secretário", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame para cadastro de Secretário
        frame_secretario = ctk.CTkFrame(self.root)
        frame_secretario.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_secretario, text="Nome do Secretário:").pack(side="left", padx=5, pady=5)

        self.entrada_secretario = ctk.CTkEntry(frame_secretario, placeholder_text="Digite o nome", width=300)
        self.entrada_secretario.pack(side="left", padx=5, pady=5)

        self.combo_secretarias = ctk.CTkComboBox(frame_secretario, values=['Selecione uma Secretaria'], width=300)
        self.combo_secretarias.pack(side="left", padx=5, pady=5)

        botao_adicionar_secretario = ctk.CTkButton(frame_secretario, text="Adicionar", command=self.adicionar_secretario, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF")
        botao_adicionar_secretario.pack(side="left", padx=5, pady=5)
        
        # Título da listagem de secretários
        ctk.CTkLabel(self.root, text="Secretarios", font=("Arial", 16, "bold")).pack(pady=10)

        # Atualiza o combobox com as secretarias disponíveis
        self.atualizar_comboboxes()

        # Frame para listagem de secretários
        frame_lista_secretarios = ctk.CTkFrame(self.root)
        frame_lista_secretarios.pack(fill="both", expand=True, padx=10, pady=5)

        self.lista_secretarios = ctk.CTkScrollableFrame(frame_lista_secretarios, width=400, height=200)
        self.lista_secretarios.pack(fill="both", expand=True)

        self.atualizar_lista_secretarios()
        # Menu secretario fim

        # Menu ata inicio
    def menu_atas(self):
            self.clear_content_frame()

            # Botão de voltar
            botao_voltar = ctk.CTkButton(self.root, text="Voltar", command=self.return_to_main_menu)
            botao_voltar.pack(anchor="nw", padx=10, pady=10)

            # Título do menu
            ctk.CTkLabel(self.root, text="Adicionar Ata", font=("Arial", 16, "bold")).pack(pady=10)

            # Frame para cadastro de Ata
            frame_ata = ctk.CTkFrame(self.root)
            frame_ata.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(frame_ata, text="Descrição da Ata:").pack(side="left", padx=5, pady=5)
            self.entrada_descricao_ata = ctk.CTkEntry(frame_ata, placeholder_text="Digite a descrição", width=300)
            self.entrada_descricao_ata.pack(side="left", padx=5, pady=5)

            ctk.CTkLabel(frame_ata, text="Data da Ata:").pack(side="left", padx=5, pady=5)
            self.entrada_data_ata = DateEntry(frame_ata, width=18, background="darkblue", foreground="white", borderwidth=2,  date_pattern='dd/MM/yyyy')
            self.entrada_data_ata.pack(side="left", padx=5, pady=5)

            ctk.CTkLabel(frame_ata, text="Horário:").pack(side="left", padx=5, pady=5)
            self.entrada_horario_inicio_menu = ctk.CTkEntry(frame_ata, placeholder_text="HH:MM", width=100)
            self.entrada_horario_inicio_menu.pack(side="left", padx=5, pady=5)

            ctk.CTkLabel(frame_ata, text="até:").pack(side="left", padx=5, pady=5)
            self.entrada_horario_termino_menu = ctk.CTkEntry(frame_ata, placeholder_text="HH:MM", width=100)
            self.entrada_horario_termino_menu.pack(side="left", padx=5, pady=5)
        
            botao_adicionar_ata = ctk.CTkButton(frame_ata, text="Adicionar", command=self.adicionar_ata, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF")
            botao_adicionar_ata.pack(side="left", padx=5, pady=5)

            # Título da listagem de atas
            ctk.CTkLabel(self.root, text="Atas", font=("Arial", 16, "bold")).pack(pady=10)

            # Frame para listagem de Atas
            frame_lista_atas = ctk.CTkFrame(self.root)
            frame_lista_atas.pack(fill="both", expand=True, padx=10, pady=5)

            self.lista_atas = ctk.CTkScrollableFrame(frame_lista_atas, width=500, height=200)
            self.lista_atas.pack(fill="both", expand=True)

            self.atualizar_lista_atas()

    def adicionar_ata(self):
        descricao = self.entrada_descricao_ata.get()
        data = self.entrada_data_ata.get()
        horario_inicio = self.entrada_horario_inicio_menu.get().strip()
        horario_termino = self.entrada_horario_termino_menu.get().strip()
        
        if not descricao or not data or not horario_inicio or not horario_termino:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        if descricao and data and horario_inicio and horario_termino:
            adicionar_ata(self.conn, descricao, data, horario_inicio, horario_termino)
            self.entrada_descricao_ata.delete(0, ctk.END)
            self.entrada_horario_inicio_menu.delete(0, ctk.END)
            self.entrada_horario_termino_menu.delete(0, ctk.END)

            messagebox.showinfo("Sucesso", "Ata adicionada, com sucesso!")
            self.atualizar_comboboxes()
            self.atualizar_lista_atas()


    def atualizar_lista_atas(self):
        for widget in self.lista_atas.winfo_children():
            widget.destroy()

        atas = listar_atas(self.conn)

        for ata in atas:
            frame = ctk.CTkFrame(self.lista_atas)
            frame.pack(fill="x", padx=5, pady=5)

            descricao = f"{ata[1]} ({ata[2]})"
            ctk.CTkLabel(frame, text=descricao).pack(side="left", padx=5)

            botao_deletar = ctk.CTkButton(frame, text="Deletar", command=lambda a_id=ata[0]: self.deletar_ata(a_id), fg_color="#dc3545", hover_color="#b02a37", text_color="#FFFFFF")
            botao_deletar.pack(side="right", padx=5)

            botao_editar = ctk.CTkButton(frame, text="Editar", command=lambda a_id=ata[0]: self.editar_ata(a_id), fg_color="#007bff", hover_color="#0056b3", text_color="#FFFFFF")
            botao_editar.pack(side="right", padx=5)

            botao_editar = ctk.CTkButton(frame, text="Exportar", command=lambda a_id=ata[0]: self.exportar_ata_ui(a_id), fg_color="#6f42c1", hover_color="#4e2a8e", text_color="#FFFFFF")
            botao_editar.pack(side="right", padx=5)

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
        janela_edicao.grab_set()

        ata_atual = [ata for ata in listar_atas(self.conn) if ata[0] == ata_id]
        if not ata_atual:
            messagebox.showerror("Erro", "Ata não encontrada.")
            janela_edicao.destroy()
            return


        descricao_atual, data_atual, horario_inicio, horario_fim = ata_atual[0][1], ata_atual[0][2], ata_atual[0][3], ata_atual[0][4]

        # Frame principal que conterá os campos de edição
        frame_campos = ctk.CTkFrame(janela_edicao)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=20)

        # Configurando linhas e colunas do grid para melhor disposição
        frame_campos.grid_columnconfigure(0, weight=1)
        frame_campos.grid_columnconfigure(1, weight=1)
        frame_campos.grid_columnconfigure(2, weight=1)
        frame_campos.grid_columnconfigure(3, weight=1)

        # --- Descrição da Ata ---
        label_descricao = ctk.CTkLabel(frame_campos, text="Descrição da Ata:")
        label_descricao.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        entrada_descricao = ctk.CTkEntry(frame_campos, width=300)
        entrada_descricao.insert(0, descricao_atual)
        entrada_descricao.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=5)

        # --- Data da Ata ---
        label_data = ctk.CTkLabel(frame_campos, text="Data da Ata:")
        label_data.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        entrada_data = DateEntry(
            frame_campos,
            width=18,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern='dd/MM/yyyy'
        )
        entrada_data.set_date(data_atual)
        entrada_data.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # --- Horário de Início ---
        label_horario_inicio = ctk.CTkLabel(frame_campos, text="Horário de Início:")
        label_horario_inicio.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        entrada_horario_inicio = ctk.CTkEntry(frame_campos, placeholder_text="HH:MM", width=100)
        entrada_horario_inicio.insert(0, horario_inicio)
        entrada_horario_inicio.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # --- Horário de Término ---
        label_horario_termino = ctk.CTkLabel(frame_campos, text="até:")
        label_horario_termino.grid(row=2, column=2, sticky="e", padx=5, pady=5)

        entrada_horario_termino = ctk.CTkEntry(frame_campos, placeholder_text="HH:MM", width=100)
        entrada_horario_termino.insert(0, horario_fim)
        entrada_horario_termino.grid(row=2, column=3, sticky="w", padx=5, pady=5)


        def salvar_edicao():
            nova_descricao = entrada_descricao.get().strip()
            nova_data = entrada_data.get().strip()
            novo_horario_inicio = self.entrada_horario_inicio.get().strip()
            novo_horario_termino = self.entrada_horario_termino.get().strip()
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

        ctk.CTkButton(janela_edicao, text="Salvar", command=salvar_edicao, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF").pack(pady=20)

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
 
    def show_success_message(self, message):
        """
        Exibe uma mensagem de sucesso em uma janela de pop-up.
        :param message: Texto da mensagem.
        """
        popup = ctk.CTkToplevel(self.root)
        popup.title("Sucesso")
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=message, wraplength=280, justify="center")
        label.pack(pady=20)
        botao_ok = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        botao_ok.pack(pady=10)


    def show_error_message(self, message):
        """
        Exibe uma mensagem de erro em uma janela de pop-up.
        :param message: Texto da mensagem.
        """
        popup = ctk.CTkToplevel(self.root)
        popup.title("Erro")
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=message, wraplength=280, justify="center", fg_color="red")
        label.pack(pady=20)
        botao_ok = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        botao_ok.pack(pady=10)



    def listar_atas(self):
        self.clear_content_frame()

        # Botão de voltar
        botao_voltar = ctk.CTkButton(self.root, text="Voltar", command=lambda: self.return_to_main_menu())
        botao_voltar.pack(anchor="nw", padx=10, pady=10)

        # Campo de busca
        frame_busca = ctk.CTkFrame(self.root)
        frame_busca.pack(fill="x", padx=10, pady=10)

        label_busca = ctk.CTkLabel(frame_busca, text="Buscar Ata:")
        label_busca.pack(side="left", padx=5)

        campo_busca = ctk.CTkEntry(frame_busca)
        campo_busca.pack(side="left", fill="x", expand=True, padx=5)

        botao_busca = ctk.CTkButton(frame_busca, text="Buscar", command=lambda: atualizar_lista(campo_busca.get()))
        botao_busca.pack(side="left", padx=5)

        # Título
        ctk.CTkLabel(self.root, text="Lista de Atas", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame para encapsular o Treeview e a Scrollbar
        frame_lista_atas = ctk.CTkFrame(self.root)
        frame_lista_atas.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar o Treeview
        lista_atas = ttk.Treeview(frame_lista_atas, columns=("Secretário", "Fala"))
        lista_atas.heading("#0", text="Ata (Descrição - Data)")
        lista_atas.heading("Secretário", text="Secretário / Secretaria")
        lista_atas.heading("Fala", text="Fala")
        lista_atas.column("Secretário", width=200)
        lista_atas.column("Fala", width=400)

        # Adicionar Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(frame_lista_atas, orient="vertical", command=lista_atas.yview)
        lista_atas.configure(yscrollcommand=scrollbar_vertical.set)

        # Posicionar o Treeview e a Scrollbar
        lista_atas.pack(side="left", fill="both", expand=True)
        scrollbar_vertical.pack(side="right", fill="y")

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
        popup.geometry("400x300")

        # Label para instrução
        label = ctk.CTkLabel(popup, text="Edite a fala:")
        label.pack(pady=10)

        # Campo de texto para edição
        texto_fala = ctk.CTkTextbox(popup, wrap="word", height=10)
        texto_fala.insert("1.0", texto_atual)  # Pré-popular com o texto atual
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
                self.show_success_message("Fala atualizada com sucesso!")    

            except Exception as e:
                # Exibe uma mensagem de erro caso algo dê errado
                self.show_error_message(f"Erro ao atualizar fala: {e}")

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

        # Botão para salvar
        botao_salvar = ctk.CTkButton(popup, text="Salvar", command=salvar_fala)
        botao_salvar.pack(pady=10)

        # Botão para cancelar
        botao_cancelar = ctk.CTkButton(popup, text="Cancelar", command=popup.destroy)
        botao_cancelar.pack(pady=10)

        # Botão para deletar
        botao_deletar = ctk.CTkButton(popup, text="Deletar", command=deletar_fala_popup, fg_color="red", hover_color="orange")
        botao_deletar.pack(pady=10)


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
