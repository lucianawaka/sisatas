import tkinter as tk
import customtkinter as ctk
from tkhtmlview import  HTMLScrolledText

class CTkHTMLScrolledText(ctk.CTkFrame):
    """
    Um widget customizado que combina um CTkFrame arredondado com um HTMLScrolledText.
    Permite ter bordas personalizadas usando CustomTkinter e a edição/renderização de HTML.
    
    Parâmetros principais de customização:
        corner_radius: define o arredondamento dos cantos do CTkFrame.
        border_color:  cor da borda do CTkFrame.
        border_width:  espessura da borda do CTkFrame.
        fg_color:      cor de fundo interna do CTkFrame.
        html:          conteúdo HTML inicial a ser exibido no HTMLScrolledText.
        
    Exemplos de uso:
        custom_html = CTkHTMLScrolledText(
            parent,
            corner_radius=10,
            border_color="#CCCCCC",
            border_width=1,
            fg_color="white",
            html="<p>Conteúdo <strong>inicial</strong></p>"
        )
        custom_html.pack(fill="both", expand=True)
    """

    def __init__(self, parent, 
                 corner_radius=10,
                 border_color="#CCCCCC",
                 border_width=1,
                 fg_color="white",
                 html=None,
                 *args, **kwargs):
        """
        Inicializa o CTkHTMLScrolledText.

        :param parent:        Container (frame ou janela) onde o widget será inserido.
        :param corner_radius: Raio de arredondamento dos cantos do frame externo.
        :param border_color:  Cor da borda do frame externo.
        :param border_width:  Espessura da borda do frame externo.
        :param fg_color:      Cor de fundo interna do frame externo.
        :param html:          String de HTML que será exibida inicialmente no HTMLScrolledText.
        :param args:          Argumentos adicionais que serão passados ao super().__init__.
        :param kwargs:        Argumentos adicionais que serão passados ao HTMLScrolledText.
        """
        super().__init__(parent, 
                         corner_radius=corner_radius, 
                         border_color=border_color, 
                         border_width=border_width, 
                         fg_color=fg_color)
        
        # Frame principal (self) já tem as bordas definidas pelo super().__init__ acima.
        # Vamos criar o HTMLScrolledText dentro dele.
        
        # Remover bordas nativas do Text do Tkinter, se desejar borda só do CTkFrame
        kwargs.setdefault("bd", 0)
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("relief", tk.FLAT)
        
        # Criar o HTMLScrolledText
        self.html_editor = HTMLScrolledText(
            self,
            html=html,
            **kwargs
        )
        self.html_editor.pack(fill="both", expand=True, padx=5, pady=5)

    def set_html(self, html: str, strip=True):
        """
        Define o conteúdo HTML no widget de texto.

        :param html:  String contendo o conteúdo HTML a ser inserido.
        :param strip: Se True, remove espaços e quebras de linha extras.
        """
        self.html_editor.set_html(html, strip=strip)

    def get_html(self):
        """
        Retorna o HTML atual do widget (se você precisar recuperar o texto em formato HTML).
        """
        # Se o seu HTMLScrolledText tiver algum método para pegar o HTML,
        # você pode usá-lo aqui. Caso contrário, implemente adequadamente.
        # Exemplo genérico:
        return self.html_editor.html_parser.get_html()

    def clear(self):
        """
        Limpa todo o conteúdo do texto.
        """
        self.html_editor.set_html("")

    def fit_height(self):
        """
        Ajusta a altura do widget para caber o conteúdo.
        """
        self.html_editor.fit_height()
