import customtkinter as ctk

class Footer:    

    def footer_container(self, main_container, image):        
            # ----------------------------------------------------------------
            # LOGO NO RODAPÉ (pode ficar ao final, fora dos “cards”)
            # ----------------------------------------------------------------
            footer_frame = ctk.CTkFrame(main_container, fg_color="#FAFAFA")
            footer_frame.pack(fill="x", pady=(30, 10))

            label_logo = ctk.CTkLabel(footer_frame, text="", image=image, compound="top")
            label_logo.pack()