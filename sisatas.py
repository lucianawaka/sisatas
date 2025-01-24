import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename
import shutil
from datetime import datetime
from tkinter import Toplevel
from tkhtmlview import HTMLLabel, HTMLScrolledText
from tkcalendar import DateEntry
from database.connection import get_connection
from database.models import create_tables
from controllers.secretaria import adicionar_secretaria, listar_secretarias
from controllers.secretario import adicionar_secretario, listar_secretarios, get_secretaria_by_secretario
from controllers.ata import adicionar_ata, listar_atas
from controllers.fala import adicionar_fala, listar_falas_por_ata, limpar_todas_as_entidades

class MeetingManagerApp:
    def __init__(self, root):
        self.conn = get_connection()
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
        botao_backup = ctk.CTkButton(frame_menu, text="Backup", command=self.realizar_backup, width=100)
        botao_backup.pack(side="right", padx=5, pady=5)

        # Botão de Carregar Backup
        botao_carregar_backup = ctk.CTkButton(frame_menu, text="Carregar Backup", command=self.carregar_backup, width=150)
        botao_carregar_backup.pack(side="right", padx=5, pady=5)

        # Label para o título do aplicativo
        label_titulo = ctk.CTkLabel(frame_menu, text="Gerenciador de Atas", font=("Arial", 18, "bold"))
        label_titulo.pack(side="left", padx=10, pady=5)

        # Frame para cadastro de Secretaria
        frame_secretaria = ctk.CTkFrame(self.root)
        frame_secretaria.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_secretaria, text="Adicionar Secretaria").pack(side="left", padx=5, pady=5)

        self.entrada_secretaria = ctk.CTkEntry(frame_secretaria, placeholder_text="Nome da Secretaria", width=200)
        self.entrada_secretaria.pack(side="left", padx=6, pady=5)

        botao_secretaria = ctk.CTkButton(frame_secretaria, text="Adicionar", command=self.adicionar_secretaria)
        botao_secretaria.pack(side="left", padx=5, pady=5)

        # Frame para cadastro de Secretário
        frame_secretario = ctk.CTkFrame(self.root)
        frame_secretario.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_secretario, text="Adicionar Secretário").pack(side="left", padx=5, pady=5)

        self.entrada_secretario = ctk.CTkEntry(frame_secretario, placeholder_text="Nome do Secretário", width=200)
        self.entrada_secretario.pack(side="left", padx=5, pady=5)

        self.combo_secretarias = ctk.CTkComboBox(frame_secretario, values=['Selectione uma Secretaria'], width=200)
        self.combo_secretarias.pack(side="left", padx=5, pady=5)

        botao_secretario = ctk.CTkButton(frame_secretario, text="Adicionar", command=self.adicionar_secretario)
        botao_secretario.pack(side="left", padx=5, pady=5)

        # Frame para cadastro de Ata
        frame_ata = ctk.CTkFrame(self.root)
        frame_ata.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame_ata, text="Adicionar Ata").pack(side="left", padx=5, pady=5)

        self.descricao_ata = ctk.CTkEntry(frame_ata, placeholder_text="Descrição da Ata", width=200)
        self.descricao_ata.pack(side="left", padx=5, pady=5)

        self.entrada_data_ata = DateEntry(frame_ata, width=18, background="darkblue", foreground="white", borderwidth=2,  date_pattern='dd/MM/yyyy')
        self.entrada_data_ata.pack(side="left", padx=5, pady=5)

        botao_ata = ctk.CTkButton(frame_ata, text="Adicionar", command=self.adicionar_ata)
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

        # Botão para listar atas
        botao_listar_atas = ctk.CTkButton(self.root, text="Listar Atas", command=self.listar_atas, fg_color="blue", hover_color="#00008B")
        botao_listar_atas.pack(side="top", padx=10, pady=5)

        self.atualizar_comboboxes()


    def return_to_main_menu(self):
        self.clear_content_frame()  # Limpa os widgets da tela de listar atas.
        self.setup_ui()  # Recria o menu principal.


    def clear_content_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def atualizar_comboboxes(self):
        # Atualizar as secretarias
        secretarias = listar_secretarias(self.conn)
        self.combo_secretarias.configure(values=[s[1] for s in secretarias])

        # Atualizar secretários com nome e secretaria
        secretarios = listar_secretarios(self.conn)
        valores_combo_secretarios = [
            f"{s[1]} ({get_secretaria_by_secretario(self.conn, s[1])})" for s in secretarios
        ]
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


    # Função para realizar backup
    def realizar_backup(self):
        try:
            # Abrir janela para o usuário selecionar a pasta
            pasta_selecionada = askdirectory(title="Selecione a pasta para salvar o backup")
            
            if not pasta_selecionada:
                # Caso o usuário cancele a seleção
                messagebox.showwarning("Backup", "Nenhuma pasta foi selecionada.")
                return

            # Gerar nome do arquivo de backup com data e hora
            nome_backup = f"backup_atas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

            # Caminho completo para salvar o backup
            caminho_backup = f"{pasta_selecionada}/{nome_backup}"

            # Criar backup do banco de dados
            shutil.copy("banco_de_dados_atas.db", caminho_backup)
            messagebox.showinfo("Backup", f"Backup realizado com sucesso em: {caminho_backup}")
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
                messagebox.showwarning("Carregar Backup", "Nenhum arquivo de backup foi selecionado.")
                return

            # Substituir o banco de dados principal pelo arquivo de backup
            caminho_principal = "banco_de_dados_atas.db"
            shutil.copy(arquivo_backup, caminho_principal)

            # Reiniciar a conexão para garantir que os dados sejam atualizados
            self.conn.close()
            self.conn = get_connection()

            # Atualizar a interface com os novos dados
            self.atualizar_comboboxes()
            messagebox.showinfo("Carregar Backup", "Backup carregado com sucesso! O sistema foi atualizado com os dados do backup.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar backup: {e}")

    # Adicionar secretaria
    def adicionar_secretaria(self):
        nome = self.entrada_secretaria.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome da secretaria não pode estar vazio.")
            return
        try:
            adicionar_secretaria(self.conn, nome)
            self.entrada_secretaria.delete(0, ctk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Secretaria adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar secretaria: {e}")


    def adicionar_secretario(self):
        nome = self.entrada_secretario.get()
        secretaria = self.combo_secretarias.get()
        if nome and secretaria:
            adicionar_secretario(self.conn, nome, secretaria)
            self.entrada_secretario.delete(0, ctk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Secretário adicionado!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def adicionar_ata(self):
        descricao = self.descricao_ata.get()
        data = self.entrada_data_ata.get()
        if descricao and data:
            adicionar_ata(self.conn, descricao, data)
            self.descricao_ata.delete(0, ctk.END)
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

    def listar_atas(self):
            self.clear_content_frame()

            # Botão de voltar
            botao_voltar = ctk.CTkButton(self.root, text="Voltar", command=lambda: self.return_to_main_menu())
            botao_voltar.pack(anchor="nw", padx=10, pady=10)

            # Criar o botão "Limpar Falas"
            botao_limpar = ctk.CTkButton(self.root, text="Limpar Falas", command=lambda: self.limpar_todas_as_entidades(), fg_color="red", hover_color="orange")
            botao_limpar.pack(pady=10)

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
            lista_atas.column("#0", width=250)
            lista_atas.column("Secretário", width=200)
            lista_atas.column("Fala", width=400)

            # Adicionar Scrollbar vertical
            scrollbar_vertical = ttk.Scrollbar(frame_lista_atas, orient="vertical", command=lista_atas.yview)
            lista_atas.configure(yscrollcommand=scrollbar_vertical.set)

            # Posicionar o Treeview e a Scrollbar
            lista_atas.pack(side="left", fill="both", expand=True)
            scrollbar_vertical.pack(side="right", fill="y")

            # Obter dados das atas e falas
            atas = listar_atas(self.conn)
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
                    secretario_nome = fala[1]  # Nome do secretário
                    secretaria_nome = get_secretaria_by_secretario(self.conn, secretario_nome)
                    secretario_completo = f"{secretario_nome} ({secretaria_nome})"
                    dados_atas[descricao_completa].append((secretario_completo, fala[2]))

            # Inserir dados no Treeview
            for descricao_completa, falas in dados_atas.items():
                item_ata = lista_atas.insert("", "end", text=f"{descricao_completa}")
                for secretario_completo, fala in falas:
                    lista_atas.insert(item_ata, "end", values=(secretario_completo, fala))

            # Função para capturar a fala selecionada e mostrar no popup
            def on_double_click(event):
                selected_item = lista_atas.selection()
                if selected_item:
                    # Obtém o texto da fala da coluna correspondente
                    fala = lista_atas.item(selected_item[0], "values")[1]
                    self.show_fala_popup(fala)

            # Associar o evento de clique duplo ao Treeview
            lista_atas.bind("<Double-1>", on_double_click)

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
