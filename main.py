import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Toplevel
from tkhtmlview import HTMLLabel, HTMLScrolledText
from tkcalendar import DateEntry
from database.connection import get_connection
from database.models import create_tables
from controllers.secretaria import adicionar_secretaria, listar_secretarias
from controllers.secretario import adicionar_secretario, listar_secretarios
from controllers.ata import adicionar_ata, listar_atas
from controllers.fala import adicionar_fala, listar_falas_por_ata, limpar_falas

class MeetingManagerApp:
    def __init__(self, root):
        self.conn = get_connection()
        self.root = root
        self.root.title("Gerenciador de Atas")
        ctk.set_appearance_mode("light")  # Tema: "light", "dark", "system"
        ctk.set_default_color_theme("green")  # Cor principal do tema
        self.setup_ui()



    def setup_ui(self):
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

        self.entrada_numero_ata = ctk.CTkEntry(frame_ata, placeholder_text="Número da Ata", width=200)
        self.entrada_numero_ata.pack(side="left", padx=5, pady=5)

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
        self.html_editor_fala.pack(anchor="w", padx=5, pady=5)

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
        secretarias = listar_secretarias(self.conn)
        self.combo_secretarias.configure(values=[s[1] for s in secretarias])

        secretarios = listar_secretarios(self.conn)
        self.combo_secretarios.configure(values=[s[1] for s in secretarios])

        atas = listar_atas(self.conn)
        self.combo_atas.configure(values=[a[1] + "- " + a[2] for a in atas])
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
        numero = self.entrada_numero_ata.get()
        data = self.entrada_data_ata.get()
        if numero and data:
            adicionar_ata(self.conn, numero, data)
            self.entrada_numero_ata.delete(0, ctk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Ata adicionada!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def adicionar_fala(self):
        ata = self.combo_atas.get().split('-')[0]
        secretario = self.combo_secretarios.get()
        fala = self.html_editor_fala.get("1.0", "end").strip()  # Captura o HTML do editor
        if ata and secretario and fala:
            adicionar_fala(self.conn, ata, secretario, fala)
            self.html_editor_fala.set_html("")  # Reseta o editor
            messagebox.showinfo("Sucesso", "Fala adicionada!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")


    def listar_atas(self):
        self.clear_content_frame()

        # Botão de voltar
        botao_voltar = ctk.CTkButton(self.root, text="Voltar", command=lambda: self.return_to_main_menu())
        botao_voltar.pack(anchor="nw", padx=10, pady=10)

        # Criar o botão "Limpar Falas"
        botao_limpar = ctk.CTkButton(self.root, text="Limpar Falas", command=lambda: limpar_falas(self.conn), fg_color="red", hover_color="orange")
        # Posicionando o botão abaixo da lista de atas
        botao_limpar.pack(pady=10)
        # Título
        ctk.CTkLabel(self.root, text="Lista de Atas", font=("Arial", 16, "bold")).pack(pady=10)

        # Obter dados das atas e falas
        atas = listar_atas(self.conn)
        dados_atas = {}
        for ata in atas:
            numero_ata = ata[0]
            data_ata = ata[2]
            dados_atas[numero_ata] = []
            falas = listar_falas_por_ata(self.conn, numero_ata)
            for fala in falas:
                dados_atas[numero_ata].append((fala[1], fala[2]))

        # Criar uma lista com rolagem
        lista_atas = ttk.Treeview(self.root, columns=("Secretário", "Fala"))
        lista_atas.heading("#0", text="Ata")
        lista_atas.heading("Secretário", text="Secretário")
        lista_atas.heading("Fala", text="Fala")
        lista_atas.pack(fill="both", expand=True)

        # Inserir dados na lista
        for numero_ata, falas in dados_atas.items():
            item_ata = lista_atas.insert("", "end", text=f"Ata {numero_ata} - {data_ata}")
            for secretario, fala in falas:
                lista_atas.insert(item_ata, "end", values=(secretario, fala))


if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    conn.close()

    root = ctk.CTk()
    app = MeetingManagerApp(root)
    root.mainloop()
