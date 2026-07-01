from modelos.classes import *
from view import *

class Controlador:
    def __init__(self, view, desenho):
        self.view = view
        self.desenho = desenho
        self.figuras = []                    # GUARDA AS FIGURAS PRONTAS
        self.figura_preview = None           # GUARDA O RASCUNHO QUE APARECE NA HORA EM QUE VOCÊ DESENHA
        self.pontos_poligono = []            # GUARDA AS COORDENADAS PARA O POLIGONO 
        self.linha_poligono = None           # GUARDA O RASCUNHO DO POLIGONO 
        self.linhas_poligono = []            # LINHAS PARA O RASCUNHO DO POLIGONO

        self.x_ini = 0
        self.y_ini = 0

        # Vincular eventos do mouse aos métodos correspondentes
        self.view.canvas.bind("<Button-1>", self.iniciar_desenho)
        self.view.canvas.bind("<B1-Motion>", self.mover_desenho)
        self.view.canvas.bind("<ButtonRelease-1>", self.terminarDesenho)
        self.view.canvas.bind("<Double-Button-1>", terminarPoligono)
        self.view.canvas.bind("<Motion>", moverPoligono)

    def iniciar_desenho(self, event):
        global x_ini, y_ini, figura_preview, pontos_poligono, linhas_poligono, linha_poligono
        self.x_ini = event.x
        self.y_ini = event.y

        # RABISCO :
        forma_atual = self.view.obter_forma()
        cor_borda = self.view.obter_cor_borda()
        cor_preenchimento = self.view.obter_cor_preench()

        if forma_atual == "Rabisco":
            figura_preview = Rabisco(x_ini, y_ini, cor_borda)
    
        elif forma_atual == "Polígono":      #SE FOR POLIGONO, APENAS SALVA OS PONTOS NA LISTA DE PONTOS
            pontos_poligono.append(x_ini)
            pontos_poligono.append(y_ini)

            if len(pontos_poligono) >= 4:
                linha_fixa = self.view.canvas.create_line(pontos_poligono[-4], pontos_poligono[-3], pontos_poligono[-2], pontos_poligono[-1])
                linhas_poligono.append(linha_fixa)
        
            linha_poligono = None
            return
    
    def mover_desenho(self, event):
        # RASCUNHO VISTO NA HORA 
        global figura_preview
        if self.view.obter_forma() == "Polígono":
            return
        x_atual = event.x
        y_atual = event.y
        
        # VALOR ESCOLHIDO MENU
        forma_atual = self.view.obter_forma()
        cor_borda = self.view.obter_cor_borda()
        cor_preenchimento = self.view.obter_cor_preench()
        
        # RABISCO SE ADICIONA APENAS O PONTO AO OBJETO
        if forma_atual == "Rabisco":
            if isinstance(figura_preview, Rabisco):
                figura_preview.adicionar_pontos(x_atual, y_atual)
        else: 
            if forma_atual == "Retângulo":
                figura_preview = Retangulo(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
            elif forma_atual == "Oval":
                figura_preview = Oval(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
            elif forma_atual == "Círculo":
                figura_preview = Circulo(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
            elif forma_atual == "Linha":
                figura_preview = Linha(x_ini, y_ini, x_atual, y_atual, cor_borda)
        
        self.desenhar_tudo()

    def mover_poligono(self, event):
        #RASCUNHO DO POLIGONO, POIS TEM UMA FORMA DIFERENTE DE SER DESENHADO
        global linha_poligono, linhas_poligono
        if self.view.obter_forma() != "Polígono":
            return
        else:
            if self.view.obter_forma()() == "Polígono" and len(pontos_poligono) >= 2:
                if linha_poligono is not None:    
                    self.view.canvas.delete(linha_poligono)
            
                x_base = pontos_poligono[-2]
                y_base = pontos_poligono[-1]
                x_atual = event.x
                y_atual = event.y

                linha_poligono = self.view.canvas.create_line(x_base, y_base, x_atual, y_atual, dash=(4,2))
            
            else:
                return
            
    
    def terminarDesenho(self, event):
        global figura_preview, linhas_poligono
        if self.view.obter_forma() == "Polígono":  #CHECAGEM PRA NÃO ATRAPALHAR A CRIAÇÃO DO POLIGONO QUANDO FOR DADO APENAS UM CLICK NO MOUSE
            return
        else:
            if figura_preview:
            # GUARDANDO NA LISTA AS FIGURAS AO SOLTAR O MOUAW
                linhas_poligono = []
                self.desenho.adicionar_figura(figura_preview)
                figura_preview = None  
                self.desenhar_tudo()

    def terminar_poligono(self, cor_borda, cor_preenchimento):
        global figura_preview, linhas_poligono
        if self.view.obter_forma() == "Polígono":
            self.pontos_poligono.pop()
            
            cor_borda = self.view.obter_cor_borda()
            cor_preenchimento = self.view.obter_cor_preench()

            figura_preview = Polígono(pontos_poligono, cor_borda, cor_preenchimento)
            for linha in linhas_poligono:
            canvas.delete(linha)  #APAGA AS LINHAS DE RASCUNHO

        canvas.delete(linha_poligono)   #APAGA A ULTIMA LINHA
        linha_poligono = None
        linhas_poligono =[]    #LIMPA A LISTA DE LINHAS

        figuras.append(figura_preview) #GUARDANDO O POLIGONO NA LISTA DE FIGURAS E DEPOIS DESENHANDO ELE
        figura_preview = None
        desenhar_tudo()

        pontos_poligono = [] #LIMPANDO A LISTA DE PONTOS PARA FICAR LIMPA PARA O PROXIMO POLIGONO
    else:
        return
    
    def desenhar_tudo(self):
        # LIMPA O CANVAS
        self.view.canvas.delete("all")
        
        # DESENHA TODAS AS FIGURAS CONCLUÍDAS
        for figura in self.desenho.figuras:
            figura.desenhar(self.view.canvas)
        
        # DESENHA O RASCUNHO ATUAL, SE HOUVER
        if figura_preview:
            figura_preview.desenhar(self.view.canvas, rascunho=True)

    def iniciar(self):
        self.view.janela.mainloop()
        




















