from tkinter import *


#Classe principal, pai de todas
class Figura:
    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
    
    def desenhar(self, canvas, rascunho=False):
        # MÉTODO EXPLICADO NA ULTIMA AULA DE GIOVANNY
        raise NotImplementedError("As subclasses precisam implementar o método desenhar()")


#Subclasses 
class Retangulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline = self.cor_borda,
            fill = self.cor_preenchimento, 
            dash = estilo_rascunho
        )

class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            fill = self.cor_preenchimento, 
            outline = self.cor_borda, 
            dash = estilo_rascunho)
        
class Circulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        largura = abs(self.x1 - self.x2)
        self.x2 = self.x1 + largura if self.x2 > self.x1 else self.x1 - largura
        self.y2 = self.y1 + largura if self.y2 > self.y1 else self.y1 - largura

    
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            fill = self.cor_preenchimento, 
            outline = self.cor_borda, 
            dash = estilo_rascunho
        )

class Rabisco(Figura):
    def __init__(self, x1, y1, cor_borda):
        super().__init__(cor_borda, cor_preenchimento = None)
        self.pontos = [(x1, y1)]
    
    def adicionar_pontos(self, x, y):
        #MÉTODO PARA O RABISCO ACUMULAR O RASTRO DEIXAD PELO MOUSE
        self.pontos.append((x, y))

    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4, 2) if rascunho else None

        if len(self.pontos) > 1:
            canvas.create_line(
                self.pontos, 
                fill=self.cor_borda, 
                dash=estilo_rascunho
            )

class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda):
        super().__init__(cor_borda, cor_preenchimento = None)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4, 2) if rascunho else None

        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill = self.cor_borda,
                           dash = estilo_rascunho)

class Poligono(Figura):
    def __init__(self, pontos, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.pontos = pontos
        
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_polygon(
            self.pontos,
            fill = self.cor_preenchimento,
            outline = self.cor_borda,
            dash = estilo_rascunho
            )