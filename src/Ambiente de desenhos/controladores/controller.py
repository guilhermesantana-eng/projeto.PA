from modelos.classes import Retangulo, Oval, Circulo, Linha, Rabisco
from view.view import desenhar_figura_na_tela  # <- Importe a função que criamos para desenhar na View
from controladores.ferramentas.retangulo_state import FerramentaRetangulo
from controladores.ferramentas.circulo_state import FerramentaCirculo
from controladores.ferramentas.oval_state import FerramentaOval
from controladores.ferramentas.linha_state import FerramentaLinha
from controladores.ferramentas.rabisco_state import FerramentaRabisco
from controladores.ferramentas.poligono_state import FerramentaPoligono


class Controlador:
    def __init__(self, view, desenho):
        self.view = view
        self.desenho = desenho

        self.ferramentas = {
            "Retângulo" : FerramentaRetangulo(),
            "Círculo" : FerramentaCirculo(),
            "Oval" : FerramentaOval(),
            "Linha" :  FerramentaLinha(),
            "Rabisco" : FerramentaRabisco(),
            "Polígono" : FerramentaPoligono()      
        }

        self.ferramenta_atual = self.ferramentas["Retângulo"]
       
        # EVENTOS DO MOUSE
        self.view.canvas.bind("<Button-1>", self.iniciar_desenho)
        self.view.canvas.bind("<B1-Motion>", self.mover_desenho)
        self.view.canvas.bind("<ButtonRelease-1>", self.terminar_desenho)
        self.view.canvas.bind("<Double-Button-1>", self.terminar_poligono)
        self.view.canvas.bind("<Motion>", self.mover_poligono)

    def iniciar_desenho(self, event):
        forma_atual = self.view.obter_forma()
        self.ferramenta_atual = self.ferramentas[forma_atual]
        self.ferramenta_atual.iniciar_desenho(self, event)

    
    def mover_desenho(self, event):
        self.ferramenta_atual.mover_desenho(self, event)

    def mover_poligono(self, event):
        #RASCUNHO DO POLIGONO, POIS TEM UMA FORMA DIFERENTE DE SER DESENHADO
        self.ferramenta_atual.mover_poligono(self, event)

    def terminar_desenho(self, event):
        self.ferramenta_atual.terminar_desenho(self, event)

    def terminar_poligono(self, event):
        self.ferramenta_atual.terminar_poligono(self, event)

    def desenhar_tudo(self):
        # LIMPA O CANVAS
        self.view.canvas.delete("all")
        
        # DESENHA TODAS AS FIGURAS CONCLUÍDAS
        for figura in self.desenho.figuras:
            desenhar_figura_na_tela(self.view.canvas, figura, rascunho=False)
        
        # DESENHA O RASCUNHO ATUAL, SE HOUVER
        if self.desenho.figura_preview:
            desenhar_figura_na_tela(self.view.canvas, self.desenho.figura_preview, rascunho=True)

    def iniciar(self):
        self.view.janela.mainloop()