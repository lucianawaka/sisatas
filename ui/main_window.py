import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import get_connection
from controllers.secretaria import adicionar_secretaria, listar_secretarias
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MainWindow:
    def __init__(self, root):
        self.conn = get_connection()
        self.root = root
        self.root.title("Gerenciador de Atas")
        self.setup_ui()

    def setup_ui(self):
        frame_secretaria = tk.LabelFrame(self.root, text="Adicionar Secretaria")
        frame_secretaria.pack(fill="x", padx=10, pady=5)

        self.entrada_secretaria = tk.Entry(frame_secretaria)
        self.entrada_secretaria.pack(side="left", padx=5, pady=5)
        # Botão para listar atas
        botao_listar_atas = tk.Button(self.root, text="Listar Atas", command=self.listar_atas)
        botao_listar_atas.pack(side="top", padx=10, pady=5)

        botao_secretaria = tk.Button(
            frame_secretaria, text="Adicionar", command=self.adicionar_secretaria
        )
        botao_secretaria.pack(side="left", padx=5, pady=5)

    def adicionar_secretaria(self):
        nome = self.entrada_secretaria.get()
        if nome:
            adicionar_secretaria(self.conn, nome)
            self.entrada_secretaria.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Secretaria adicionada!")
        else:
            messagebox.showerror("Erro", "Nome não pode estar vazio.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
