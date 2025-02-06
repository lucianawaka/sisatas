import customtkinter as ctk

class Containers():
        
        def container_pages(self):
            self.clear_content_frame()

            self.root.configure(bg="#FAFAFA")
                # Frame principal ocupando toda a janela
            main_container = ctk.CTkFrame(self.root, fg_color="#FAFAFA")
            main_container.pack(fill="both", expand=True)

            # Frame para botão no topo
            header_frame = ctk.CTkFrame(main_container, fg_color="#FAFAFA")
            header_frame.pack(fill="x", pady=(20, 10), padx=390)

            return main_container, header_frame
