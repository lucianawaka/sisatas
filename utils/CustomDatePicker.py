import customtkinter as ctk
import calendar
from datetime import datetime, date
from utils.images import load_icons

class CustomDatePicker(ctk.CTkFrame):
    def __init__(self, master=None, width=150, height=48, **kwargs):
        """CustomDatePicker: um campo de entrada + botão para abrir um calendário."""
        super().__init__(master, **kwargs)
        self.icons = load_icons()
        # Definindo data selecionada como "hoje"
        today = datetime.today()
        self.selected_date = today.strftime("%d/%m/%Y")

        # Campo de texto (CTkEntry) - subtraímos 40 do width para acomodar o botão "📅"
        self.entry = ctk.CTkEntry(
            self,
            width=width - 40,
            height=height,
            placeholder_text="DD/MM/AAAA",
            corner_radius=10,
            border_width=1,
            border_color="#CCC",
            fg_color="white",
            text_color="#333"
        )
        # Não usar fill="y" se queremos fixar height
        self.entry.pack(side="left")

        # Exibe a data de hoje no entry
        self.entry.insert(0, self.selected_date)

        # Botão para abrir o calendário
        self.open_button = ctk.CTkButton(
            self,
            image=self.icons["calendar"],
            text="",
            width=40,          # Botão fica com largura fixa
            height=height,     # Mesma altura do entry
            corner_radius=10,
            fg_color="#019000",
            command=self.open_calendar
        )
        self.open_button.pack(side="left")

        # Variáveis de controle do mês/ano exibidos no calendário
        self.current_year = None
        self.current_month = None
        self.top = None  # Referência ao popup
    def set_selected_date(self, date_str):
        """Atualiza a data selecionada."""
        self.selected_date = date_str
    def open_calendar(self):
        # Se a janela já estiver aberta, destrói para recriar
        if self.top is not None and self.top.winfo_exists():
            try:
                self.top.destroy()
            except:
                pass

        # Posição para abrir o calendário logo abaixo do botão
        x = self.open_button.winfo_rootx()
        y = self.open_button.winfo_rooty() + self.open_button.winfo_height()

        # Cria o popup Toplevel
        self.top = ctk.CTkToplevel(self)
        self.top.title("Selecione a Data")
        self.top.geometry(f"+{x}+{y}")
        self.top.attributes("-topmost", True)

        # Define o mês/ano atuais
        today = datetime.today()
        self.current_year = today.year
        self.current_month = today.month

        self.calendar_frame = ctk.CTkFrame(self.top)
        self.calendar_frame.pack(padx=5, pady=5)

        self.draw_calendar()

    def draw_calendar(self):
        # Limpa o frame do calendário antes de desenhar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # ===== Cabeçalho de navegação (mês/ano) =====
        nav_frame = ctk.CTkFrame(self.calendar_frame)
        nav_frame.pack()

        prev_button = ctk.CTkButton(nav_frame, text="<", width=30,
                                    command=self.go_prev_month)
        prev_button.pack(side="left", padx=2)

        label_month = ctk.CTkLabel(
            nav_frame,
            text=f"{self.current_month:02d}/{self.current_year}",
            font=("Arial", 14, "bold")
        )
        label_month.pack(side="left", padx=10)

        next_button = ctk.CTkButton(nav_frame, text=">", width=30,
                                    command=self.go_next_month)
        next_button.pack(side="left", padx=2)

        # ===== Cabeçalho dos dias da semana =====
        days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        header_frame = ctk.CTkFrame(self.calendar_frame)
        header_frame.pack(pady=5)

        for d in days_of_week:
            lbl = ctk.CTkLabel(header_frame, text=d, width=5)
            lbl.pack(side="left", padx=5)

        # ===== Dias do mês =====
        days_frame = ctk.CTkFrame(self.calendar_frame)
        days_frame.pack()

        cal = calendar.Calendar(firstweekday=0)  # 0=Monday
        month_days = list(cal.itermonthdays(self.current_year, self.current_month))

        row = 0
        col = 0
        for day in month_days:
            if day == 0:
                # Dias fora do mês retornam 0
                blank = ctk.CTkLabel(days_frame, text="", width=5)
                blank.grid(row=row, column=col, padx=4, pady=4)
            else:
                day_btn = ctk.CTkButton(
                    days_frame,
                    text=str(day),
                    width=30,
                    command=lambda d=day: self.select_day(d)
                )
                day_btn.grid(row=row, column=col, padx=4, pady=4)

            col += 1
            if col == 7:
                col = 0
                row += 1

    def select_day(self, day):
        chosen_date = datetime(self.current_year, self.current_month, day)
        self.selected_date = chosen_date.strftime("%d/%m/%Y")
        self.entry.delete(0, "end")
        self.entry.insert(0, self.selected_date)
        self.top.destroy()  # Fecha o pop-up

    def go_prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    def go_next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()


    def set_date(self, value):
        """
        Define o valor de data.
        value pode ser 'YYYY-MM-DD' (string), datetime.date, datetime.datetime, etc.
        """
        if isinstance(value, (date, datetime)):
            # Se for objeto date/datetime, só formatamos
            self.selected_date = value.strftime("%d/%m/%Y")
        else:
            # Se vier como string '2025-04-17', convertemos
            if isinstance(value, str):
                try:
                    dt = datetime.strptime(value, "%Y-%m-%d")
                    self.selected_date = dt.strftime("%d/%m/%Y")
                except ValueError:
                    # Se não for no formato YYYY-MM-DD, guardamos a string “como está”
                    self.selected_date = value
            else:
                self.selected_date = str(value)

        # ATUALIZA O ENTRY AQUI:
        self.entry.delete(0, "end")
        self.entry.insert(0, self.selected_date)


             
    def get(self):
        """ Retorna a data atualmente exibida no campo de texto. """
        return self.entry.get()
