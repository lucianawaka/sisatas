import customtkinter as ctk

class Botoes:
    
    def btn_voltar(self, header_frame):
        # Botão de voltar
        botao_voltar = ctk.CTkButton(
            header_frame, 
            text="Voltar", 
            image=self.icons["voltar"],  # pega o ícone do dicionário
            compound="left",
            width=114,
            height=48,
            fg_color="#007E37",
            hover_color="#005C29",
            text_color="#FFFFFF",
            corner_radius=8,
            font=("Arial", 16),
            command=lambda: self.return_to_main_menu())
        botao_voltar.pack(anchor="nw", padx=10, pady=10)