import customtkinter as ctk
from utils.CustomDatePicker import CustomDatePicker
class CriarAta():

    def criar_ata(self, main_container):
          # ----------------------------------------------------------------
        # PRIMEIRO BLOCO EM BRANCO: “Criação de Ata”
        # ----------------------------------------------------------------
        card_ata = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10)
        card_ata.pack(fill="x", padx=400, pady=(20, 20))

        # ---------- Seção: Criação de Ata ----------
        section_ata = ctk.CTkFrame(card_ata, fg_color="white")
        section_ata.pack(fill="x", pady=(10, 10))

        label_ata = ctk.CTkLabel(
            section_ata,
            text="Criação de Ata",
            font=("Montserrat", 22, "bold"),
            text_color="#007E37"
        )
        label_ata.pack(anchor="w", pady=(0, 5), padx=10)

        # Frame único para agrupar os campos em linha
        row_ata = ctk.CTkFrame(section_ata, fg_color="white")
        row_ata.pack(fill="x")

        # Campo "Nome da Ata"
        self.descricao_ata = ctk.CTkEntry(
            row_ata, 
            placeholder_text="Nome da Ata", 
            width=380,
            height=48,
            corner_radius=10,
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            font=("Montserrat", 16)
        )
        self.descricao_ata.pack(side="left", padx=15, pady=5)

        # Campo de data (DatePicker customizado)
        # -> Não crie outro root, use simplesmente 'row_ata' como parent
        self.entrada_data_ata = CustomDatePicker(
            row_ata, 
            width=140, 
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
            font=("Montserrat", 12, "bold"),
            text_color="#007E37"
        )
        label_inicio.pack(side="left", padx=(20,5), pady=5)

        # Campo "Horário de Início"
        self.entrada_horario_inicio = ctk.CTkEntry(
            row_ata,
            placeholder_text="HH:MM",
            width=70,
            height=48,
            corner_radius=10,
            font=("Montserrat", 14),
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
            font=("Montserrat", 12, "bold"),
            text_color="#007E37"
        )
        label_termino.pack(side="left", padx=(20,5), pady=5)

        # Campo "Horário de Término"
        self.entrada_horario_termino = ctk.CTkEntry(
            row_ata,
            placeholder_text="HH:MM",
            width=70,
            height=48,
            corner_radius=10,
            font=("Montserrat", 14),
            border_width=1,
            border_color="#CCCCCC",
            fg_color="white",
            text_color="#333333"
        )
        self.entrada_horario_termino.pack(side="left", padx=5, pady=5)

        # Botão "+ Nova Ata" (fica à extrema direita)
        botao_nova_ata = ctk.CTkButton(
            row_ata, 
            image=self.icons["nova_ata"],
            text="Nova Ata",
            fg_color="#019000",
            text_color="#FFFFFF",
            hover_color="#007E37",
            compound="left",
            width=156,
            height=48,
            font=("Montserrat", 16, "bold"),
            command=self.adicionar_ata_principal
        )
        botao_nova_ata.pack(side="right", padx=10, pady=5)
