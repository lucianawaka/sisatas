import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import get_connection
from database.models import create_tables
from tkcalendar import DateEntry
from controllers.secretaria import adicionar_secretaria, listar_secretarias
from controllers.secretario import adicionar_secretario, listar_secretarios
from controllers.ata import adicionar_ata, listar_atas
from controllers.fala import adicionar_fala, listar_falas_por_ata

class MeetingManagerApp:
    def __init__(self, root):
        self.conn = get_connection()
        self.root = root
        self.root.title("Gerenciador de Atas")
        self.setup_ui()

    def setup_ui(self):
        # Frame para cadastro de Secretaria
        frame_secretaria = tk.LabelFrame(self.root, text="Adicionar Secretaria")
        frame_secretaria.pack(fill="x", padx=10, pady=5)

        self.entrada_secretaria = tk.Entry(frame_secretaria)
        self.entrada_secretaria.pack(side="left", padx=5, pady=5)

        botao_secretaria = tk.Button(frame_secretaria, text="Adicionar", command=self.adicionar_secretaria)
        botao_secretaria.pack(side="left", padx=5, pady=5)

        # Frame para cadastro de Secretário
        frame_secretario = tk.LabelFrame(self.root, text="Adicionar Secretário")
        frame_secretario.pack(fill="x", padx=10, pady=5)

        self.entrada_secretario = tk.Entry(frame_secretario)
        self.entrada_secretario.pack(side="left", padx=5, pady=5)

        self.combo_secretarias = ttk.Combobox(frame_secretario)
        self.combo_secretarias.pack(side="left", padx=5, pady=5)

        botao_secretario = tk.Button(frame_secretario, text="Adicionar", command=self.adicionar_secretario)
        botao_secretario.pack(side="left", padx=5, pady=5)

        # Frame para cadastro de Ata
        frame_ata = tk.LabelFrame(self.root, text="Adicionar Ata")
        frame_ata.pack(fill="x", padx=10, pady=5)

        self.entrada_numero_ata = tk.Entry(frame_ata)
        self.entrada_numero_ata.pack(side="left", padx=5, pady=5)
        
        self.entrada_data_ata = DateEntry(frame_ata, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', locale='pt_BR')
        self.entrada_data_ata.pack(side="left", padx=5, pady=5)

        botao_ata = tk.Button(frame_ata, text="Adicionar", command=self.adicionar_ata)
        botao_ata.pack(side="left", padx=5, pady=5)

        # Frame para registro de Falas
        frame_fala = tk.LabelFrame(self.root, text="Adicionar Fala")
        frame_fala.pack(fill="x", padx=10, pady=5)

        self.combo_atas = ttk.Combobox(frame_fala)
        self.combo_atas.pack(side="left", padx=5, pady=5)

        self.combo_secretarios = ttk.Combobox(frame_fala)
        self.combo_secretarios.pack(side="left", padx=5, pady=5)

        self.entrada_fala = tk.Entry(frame_fala)
        self.entrada_fala.pack(side="left", padx=5, pady=5)

        botao_fala = tk.Button(frame_fala, text="Adicionar", command=self.adicionar_fala)
        botao_fala.pack(side="left", padx=5, pady=5)

        # Botão para listar atas
        botao_listar_atas = tk.Button(self.root, text="Listar Atas", command=self.listar_atas)
        botao_listar_atas.pack(side="top", padx=10, pady=5)

        self.atualizar_comboboxes()

    def adicionar_secretaria(self):
        nome = self.entrada_secretaria.get()
        if nome:
            adicionar_secretaria(self.conn, nome)
            self.entrada_secretaria.delete(0, tk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Secretaria adicionada!")
        else:
            messagebox.showerror("Erro", "Nome não pode estar vazio.")

    def adicionar_secretario(self):
        nome = self.entrada_secretario.get()
        secretaria = self.combo_secretarias.get()
        if nome and secretaria:
            adicionar_secretario(self.conn, nome, secretaria)
            self.entrada_secretario.delete(0, tk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Secretário adicionado!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def adicionar_ata(self):
        numero = self.entrada_numero_ata.get()
        data = self.entrada_data_ata.get()
        if numero and data:
            adicionar_ata(self.conn, numero, data)
            self.entrada_numero_ata.delete(0, tk.END)
            self.entrada_data_ata.delete(0, tk.END)
            self.atualizar_comboboxes()
            messagebox.showinfo("Sucesso", "Ata adicionada!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def adicionar_fala(self):
        ata = self.combo_atas.get()
        secretario = self.combo_secretarios.get()
        fala = self.entrada_fala.get()
        if ata and secretario and fala:
            adicionar_fala(self.conn, ata, secretario, fala)
            self.entrada_fala.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Fala adicionada!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def listar_atas(self):
        self.clear_content_frame()

        tk.Label(self.root, text="Lista de Atas").pack(pady=10)

        atas = listar_atas(self.conn)  # Lista todas as atas
        for ata in atas:
            tk.Label(
                self.root, text=f"Ata: {ata[1]} - Data: {ata[2]}", font=("Arial", 12, "bold")
            ).pack(anchor="w", pady=5)

            # Busca falas relacionadas à ata
            falas = listar_falas_por_ata(self.conn, ata[0])
            if falas:
                for fala in falas:
                    tk.Label(
                        self.root,
                        text=f"  Secretário: {fala[1]} - Fala: {fala[2]}",
                        font=("Arial", 10),
                    ).pack(anchor="w", padx=20)
            else:
                tk.Label(
                    self.root, text="  Nenhuma fala registrada.", font=("Arial", 10, "italic")
                ).pack(anchor="w", padx=20)

    def clear_content_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def atualizar_comboboxes(self):
        # Atualiza as secretarias no combobox
        secretarias = listar_secretarias(self.conn)
        self.combo_secretarias["values"] = [s[1] for s in secretarias]

        # Atualiza os secretários no combobox
        secretarios = listar_secretarios(self.conn)
        self.combo_secretarios["values"] = [s[1] for s in secretarios]

        # Atualiza as atas no combobox
        atas = listar_atas(self.conn)
        self.combo_atas["values"] = [a[1] for a in atas]

if __name__ == "__main__":
    # Inicializa o banco de dados
    conn = get_connection()
    create_tables(conn)
    conn.close()

    # Inicia a interface gráfica
    root = tk.Tk()
    app = MeetingManagerApp(root)
    root.mainloop()
