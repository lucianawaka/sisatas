import customtkinter as ctk
import tkinter as tk
import os  # Importação necessária para usar funções de sistema de arquivos
from tkinter import messagebox
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
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

class MeetingManagerApp:
    def __init__(self, root):
        self.conn = get_connection()
        #atualizar_banco(self.conn)
        self.root = root
        self.root.title("Gerenciador de Atas")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.update_idletasks()  # Garante que o tkinter atualize as dimensões da janela
        ctk.set_appearance_mode("light")  # Tema: "light", "dark", "system"
        ctk.set_default_color_theme("green")  # Cor principal do tema
        self.setup_ui()



    def setup_ui(self):

        # Frame para o menu horizontal
        frame_menu = ctk.CTkFrame(self.root, height=50)
        frame_menu.pack(fill="x", padx=10, pady=5)

        # Botão de Backup
        botao_backup = ctk.CTkButton(frame_menu, text="Exportar dados", command=self.realizar_backup, width=150,fg_color="#dc3545", hover_color="#a71d2a", text_color="#FFFFFF")
        botao_backup.pack(side="right", padx=5, pady=5)

        # Botão de Importar dados
        botao_carregar_backup = ctk.CTkButton(frame_menu, text="Importar dados", command=self.carregar_backup, width=150, fg_color="#6f42c1", hover_color="#4e2a8e", text_color="#FFFFFF")
        botao_carregar_backup.pack(side="right", padx=5, pady=5)

        # Botão de Carregar Menu da Secretario
        botao_secretario_menu = ctk.CTkButton(frame_menu, text="Secretarios", command=self.menu_secretario, width=150, fg_color="#fd7e14", hover_color="#e56406", text_color="#FFFFFF")
        botao_secretario_menu.pack(side="right", padx=5, pady=5)

        # Botão de Carregar Menu da Secretaria
        botao_secretaria_menu = ctk.CTkButton(frame_menu, text="Secretarias", command=self.menu_secretaria, width=150, fg_color="#28a745", hover_color="#1e7e34", text_color="#FFFFFF")
        botao_secretaria_menu.pack(side="right", padx=5, pady=5)

        # Botão de Carregar Menu da Atas
        botao_atas_menu = ctk.CTkButton(frame_menu, text="Atas", command=self.menu_atas, width=150, fg_color="#17a2b8", hover_color="#117a8b", text_color="#FFFFFF")
        botao_atas_menu.pack(side="right", padx=5, pady=5)

        # Botão de Listar Atas
        botao_listar_atas = ctk.CTkButton(frame_menu, text="Listar Atas", command=self.listar_atas, width=150, fg_color="#007BFF", hover_color="#0056b3", text_color="#FFFFFF")
        botao_listar_atas.pack(side="right", padx=5, pady=5)

        # Label para o título do aplicativo
        label_titulo = ctk.CTkLabel(frame_menu, text="Gerenciador de Atas", font=("Arial", 18, "bold"))
        label_titulo.pack(side="left", padx=10, pady=5)

        # Frame para cadastro de Ata
        frame_ata = ctk.CTkFrame(self.root)
        frame_ata.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_ata, text="Adicionar Ata").pack(side="left", padx=5, pady=5)

        self.descricao_ata = ctk.CTkEntry(frame_ata, placeholder_text="Descrição da Ata", width=200)
        self.descricao_ata.pack(side="left", padx=5, pady=5)

        self.entrada_data_ata = DateEntry(frame_ata, width=18, background="darkblue", foreground="white", borderwidth=2,  date_pattern='dd/MM/yyyy')
        self.entrada_data_ata.pack(side="left", padx=5, pady=5)
        
        ctk.CTkLabel(frame_ata, text="Horário de Início:").pack(side="left", padx=5, pady=5)
        self.entrada_horario_inicio = ctk.CTkEntry(frame_ata, placeholder_text="HH:MM", width=100)
        self.entrada_horario_inicio.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(frame_ata, text="Horário de Término:").pack(side="left", padx=5, pady=5)
        self.entrada_horario_termino = ctk.CTkEntry(frame_ata, placeholder_text="HH:MM", width=100)
        self.entrada_horario_termino.pack(side="left", padx=5, pady=5)

        botao_ata = ctk.CTkButton(frame_ata, text="Adicionar", command=self.adicionar_ata_principal)
        botao_ata.pack(side="left", padx=5, pady=5)

        # Frame para registro de Falas
        frame_fala = ctk.CTkFrame(self.root)
        frame_fala.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_fala, text="Adicionar Fala", font=("Arial", 14, "bold")).pack(anchor="w", padx=5, pady=5)

        # Frame interno para organizar os ComboBox lado a lado
        frame_combos = ctk.CTkFrame(frame_fala)
        frame_combos.pack(anchor="w", fill="x", padx=5, pady=5)

        self.combo_atas = ctk.CTkComboBox(frame_combos, values=['Selecione uma Ata'], width=250)
        self.combo_atas.pack(side="left", padx=5, pady=5)

        self.combo_secretarios = ctk.CTkComboBox(frame_combos, values=['Selecione um Secretário'], width=250)
        self.combo_secretarios.pack(side="left", padx=5, pady=5)

        # Editor HTML para a fala
        self.html_editor_fala = HTMLScrolledText(frame_fala, html="", height=16, width=80)
        self.html_editor_fala.pack(anchor="w", padx=5, pady=5,fill="both", expand=True)

        # Botão de Adicionar Fala
        botao_fala = ctk.CTkButton(frame_fala, text="Adicionar Fala", command=self.adicionar_fala, width=150)
        botao_fala.pack(anchor="center", padx=5, pady=5)



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
        if descricao and data:
            adicionar_ata(self.conn, descricao, data, horario_inicio, horario_termino)
            self.descricao_ata.delete(0, ctk.END)
            self.entrada_data_ata.delete(0, ctk.END)
            self.entrada_horario_inicio.delete(0, ctk.END)
            self.entrada_horario_termino.delete(0, ctk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Ata adicionada!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def adicionar_fala(self):
        ata = self.combo_atas.get().split('-')[0].strip()  # Captura apenas a descrição da ata
        secretario = self.combo_secretarios.get().split(' (')[0].strip()  # Captura apenas o nome do secretário
        fala = self.html_editor_fala.get("1.0", "end").strip()  # Captura o HTML do editor

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

            ctk.CTkLabel(frame_ata, text="Horário de Início:").pack(side="left", padx=5, pady=5)
            self.entrada_horario_inicio = ctk.CTkEntry(frame_ata, placeholder_text="HH:MM", width=100)
            self.entrada_horario_inicio.pack(side="left", padx=5, pady=5)

            ctk.CTkLabel(frame_ata, text="Horário de Término:").pack(side="left", padx=5, pady=5)
            self.entrada_horario_termino = ctk.CTkEntry(frame_ata, placeholder_text="HH:MM", width=100)
            self.entrada_horario_termino.pack(side="left", padx=5, pady=5)
        
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
        horario_inicio = self.entrada_horario_inicio.get().strip()
        horario_termino = self.entrada_horario_termino.get().strip()
        
        if not descricao or not data or not horario_inicio or not horario_termino:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        if descricao and data:
            adicionar_ata(self.conn, descricao, data, horario_inicio, horario_termino)
            self.entrada_descricao_ata.delete(0, ctk.END)
            self.entrada_horario_inicio.delete(0, ctk.END)
            self.entrada_horario_termino.delete(0, ctk.END)

            messagebox.showinfo("Sucesso", "Ata adicionada, com sucesso!")
            #self.atualizar_comboboxes()
            self.atualizar_lista_atas()


        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

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
        """
        Função da camada de UI que gera o PDF da ata.
        Chama a função do controller para obter os dados e,
        em seguida, gera o PDF conforme a estrutura definida.

        Estrutura do PDF:
        - Título: Nome (descrição) da ata e data.
        - Secretários participantes (em ordem alfabética).
        - Falas: Cada fala com o nome do secretário antes.
        """
    # Obtém os dados da ata e as falas; se a ata não existir, uma exceção será lançada.
        try:
            descricao, data, falas, horario_inicio, horario_termino = obter_dados_ata(self.conn, ata_id)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return

        # Pergunta ao usuário qual pasta deseja salvar o PDF.
        pasta_destino = filedialog.askdirectory(title="Selecione a pasta para salvar o PDF")
        if not pasta_destino:
            # Se o usuário cancelar a seleção, encerra a função.
            return

        # Define o caminho completo para o arquivo PDF
        filename = os.path.join(pasta_destino, f"ata_{descricao}.pdf")
        
        # Agrupa as falas por secretário.
        secretarios_dict = {}
        for fala in falas:
            # Cada registro: (id, secretario, fala)
            _, secretario, fala_texto = fala
            if secretario not in secretarios_dict:
                secretarios_dict[secretario] = []
            secretarios_dict[secretario].append(fala_texto)

        # Ordena os secretários em ordem alfabética.
        secretarios_ordenados = sorted(secretarios_dict.items(), key=lambda x: x[0])

        # Cria o PDF usando ReportLab.
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        margin = 50
        y = height - margin

        # --- Título ---
        c.setFont("Helvetica-Bold", 16)
        titulo = f"{descricao} - {data} - {horario_inicio} - {horario_termino}"
        c.drawString(margin, y, titulo)
        y -= 30

        # --- Seção: Secretários participantes ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "Secretários participantes:")
        y -= 20
        c.setFont("Helvetica", 12)
        for secretario, _ in secretarios_ordenados:
            c.drawString(margin + 20, y, secretario)
            y -= 15
            if y < margin:
                c.showPage()
                y = height - margin
                c.setFont("Helvetica", 12)
        y -= 10

        # --- Seção: Falas ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, "Falas:")
        y -= 20
        c.setFont("Helvetica", 12)
        for secretario, falas_list in secretarios_ordenados:
            for fala_texto in falas_list:
                # Concatena o nome do secretário com o texto da fala.
                fala_completa = f"{secretario}: {fala_texto}"
                # Utiliza textwrap para quebrar o texto em linhas, se necessário.
                linhas = textwrap.wrap(fala_completa, width=100)
                for linha in linhas:
                    c.drawString(margin, y, linha)
                    y -= 15
                    if y < margin:
                        c.showPage()
                        y = height - margin
                        c.setFont("Helvetica", 12)
                y -= 5  # Espaço extra entre as falas

        c.save()
        messagebox.showinfo("Sucesso", f"PDF exportado com sucesso:\n{filename}")
    # Fim exportar ata



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

        ctk.CTkLabel(janela_edicao, text="Descrição da Ata:").pack(pady=10)
        entrada_descricao = ctk.CTkEntry(janela_edicao, width=300)
        entrada_descricao.insert(0, descricao_atual)
        entrada_descricao.pack(pady=5)

        ctk.CTkLabel(janela_edicao, text="Data da Ata:").pack(pady=10)
        entrada_data = DateEntry(janela_edicao, width=18, background="darkblue", foreground="white", borderwidth=2, date_pattern='dd/MM/yyyy')
        entrada_data.set_date(data_atual)
        entrada_data.pack(pady=5)


        ctk.CTkLabel(janela_edicao, text="Horário de Início:").pack(side="left", padx=10)
        self.entrada_horario_inicio = ctk.CTkEntry(janela_edicao, placeholder_text="HH:MM", width=100)
        self.entrada_horario_inicio.insert(0, horario_inicio)
        self.entrada_horario_inicio.pack(side="left", padx=5)

        ctk.CTkLabel(janela_edicao, text="Horário de Término:").pack(side="left", padx=10)
        self.entrada_horario_termino = ctk.CTkEntry(janela_edicao, placeholder_text="HH:MM", width=100)
        self.entrada_horario_termino.insert(0, horario_fim)
        self.entrada_horario_termino.pack(side="left", padx=5)

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

        # Criar o botão "Limpar Falas"
        # botao_limpar = ctk.CTkButton(self.root, text="Limpar Falas", command=lambda: self.limpar_todas_as_entidades(), fg_color="red", hover_color="orange")
        # botao_limpar.pack(pady=10)

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
        lista_atas = ttk.Treeview(frame_lista_atas, columns=( "Secretário", "Fala"))
        lista_atas.heading("#0", text="Ata (Descrição - Data)")
        lista_atas.heading("Secretário", text="Secretário / Secretaria")
        lista_atas.heading("Fala", text="Fala")
        #lista_atas.column("#0", width=250)
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

            # Atualizar Treeview com atas filtradas
            dados_atas = {}
            for ata in atas:
                numero_ata = ata[0]
                descricao_ata = ata[1]
                data_ata = ata[2]
                descricao_completa = f"{descricao_ata} - {data_ata}"
                dados_atas[descricao_completa] = []

                # Obter falas vinculadas à ata
                falas = listar_falas_por_ata(self.conn, numero_ata)
                for fala in falas:
                    #fala_id = fala[0]
                    secretario_nome = fala[1]  # Nome do secretário
                    secretaria_nome = get_secretaria_by_secretario(self.conn, secretario_nome)
                    secretario_completo = f"{secretario_nome} ({secretaria_nome})"
                    dados_atas[descricao_completa].append((secretario_completo, fala[2]))

            # Inserir dados no Treeview
            for descricao_completa, falas in dados_atas.items():
                item_ata = lista_atas.insert("", "end", text=f"{descricao_completa}")
                for secretario_completo, fala_texto in falas:
                    lista_atas.insert(item_ata, "end", values=(secretario_completo, fala_texto))

        # Inicializar a lista de atas
        atualizar_lista("")

        # Função para capturar a fala selecionada e mostrar no popup
        def on_double_click(event):
            selected_item = lista_atas.selection()
            if selected_item:
                fala_data = lista_atas.item(selected_item[0], "values")
                if fala_data:
                    fala_id = fala_data[0]  # ID da fala
                    texto_atual = fala_data[2]  # Texto da fala
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
            novo_texto = texto_fala.get("1.0", "end").strip()  # Captura o texto editado
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
