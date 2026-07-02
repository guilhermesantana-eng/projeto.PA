from modelos.classes import Retangulo, Oval, Circulo, Linha, Rabisco
from view.view import desenhar_figura_na_tela  # <- Importe a função que criamos para desenhar na View

class Controlador:
    def __init__(self, view, desenho):
        self.view = view
        self.desenho = desenho

        self.x_ini = 0
        self.y_ini = 0

        # RASCUNHO DE LINHA DO POLÍGONO
        self.linha_poligono_temp = None           
        self.linhas_poligono_fixas_temp = []      

        # EVENTOS DO MOUSE
        self.view.canvas.bind("<Button-1>", self.iniciar_desenho)
        self.view.canvas.bind("<B1-Motion>", self.mover_desenho)
        self.view.canvas.bind("<ButtonRelease-1>", self.terminar_desenho)
        self.view.canvas.bind("<Double-Button-1>", self.terminar_poligono)
        self.view.canvas.bind("<Motion>", self.mover_poligono)

    def iniciar_desenho(self, event):
        self.x_ini = event.x
        self.y_ini = event.y

        forma_atual = self.view.obter_forma()
        cor_borda = self.view.obter_cor_borda()

        if forma_atual == "Rabisco":
            self.desenho.figura_preview = Rabisco(self.x_ini, self.y_ini, cor_borda)
    
        elif forma_atual == "Polígono":
            # GUARDA O PONTO CLICADO PELO MODELO LÁ DO ARQUIVO DESENHO.PY
            self.desenho.adicionar_ponto_poligono(self.x_ini, self.y_ini)

            # SE JÁ TEM DOIS OU MAIS PONTOS CLICADOS
            if len(self.desenho.pontos_poligono) >= 4:
                linha_fixa = self.view.canvas.create_line(
                    self.desenho.pontos_poligono[-4], self.desenho.pontos_poligono[-3], 
                    self.desenho.pontos_poligono[-2], self.desenho.pontos_poligono[-1]
                )
                self.linhas_poligono_fixas_temp.append(linha_fixa)
        
            self.linha_poligono_temp = None
    
    def mover_desenho(self, event):
        # RASCUNHO VISTO NA HORA 
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
            if isinstance(self.desenho.figura_preview, Rabisco):
                self.desenho.figura_preview.adicionar_pontos(x_atual, y_atual)
        else: 
            if forma_atual == "Retângulo":
                self.desenho.figura_preview = Retangulo(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
            elif forma_atual == "Oval":
                self.desenho.figura_preview = Oval(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
            elif forma_atual == "Círculo":
                self.desenho.figura_preview = Circulo(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
            elif forma_atual == "Linha":
                self.desenho.figura_preview = Linha(self.x_ini, self.y_ini, x_atual, y_atual, cor_borda)
        
        self.desenhar_tudo()

    def mover_poligono(self, event):
        #RASCUNHO DO POLIGONO, POIS TEM UMA FORMA DIFERENTE DE SER DESENHADO
        if self.view.obter_forma() != "Polígono":
            return
            
        # DESENHA LINHA QUE SEGUE O MOUSE
        if len(self.desenho.pontos_poligono) >= 2:
            if self.linha_poligono_temp is not None:    
                self.view.canvas.delete(self.linha_poligono_temp)
        
            x_base = self.desenho.pontos_poligono[-2]
            y_base = self.desenho.pontos_poligono[-1]
            x_atual = event.x
            y_atual = event.y

            self.linha_poligono_temp = self.view.canvas.create_line(x_base, y_base, x_atual, y_atual, dash=(4,2))
            
    def terminar_desenho(self, event):
        if self.view.obter_forma() == "Polígono":
            return
            
        if self.desenho.figura_preview:
            # SALVA NO BANCO DE DADOS DO MODELO
            self.desenho.adicionar_figura(self.desenho.figura_preview)
            self.desenho.reiniciar_preview()  
            self.desenhar_tudo()

    def terminar_poligono(self, event):
        if self.view.obter_forma() != "Polígono":
            return
            
        cor_borda = self.view.obter_cor_borda()
        cor_preenchimento = self.view.obter_cor_preench()

        # NO MODELO DESENHOS HÁ UMA FUNÇÃO QUE LIMPA O CLIQUE DUPLO, AQUI ESTÁ SENDO USADA ELA
        self.desenho.finalizar_poligono(cor_borda, cor_preenchimento)

        # APAGA AS LINAHS PRETAS E TEMPORÁRIAS
        for linha in self.linhas_poligono_fixas_temp:
            self.view.canvas.delete(linha)  
        if self.linha_poligono_temp:
            self.view.canvas.delete(self.linha_poligono_temp)

        # RESETA OS RASCUNHOS
        self.linha_poligono_temp = None
        self.linhas_poligono_fixas_temp = []

        # REFAZ A TELA COM O NOVO POLÍGONO VINDO DO MODELO
        self.desenhar_tudo()

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