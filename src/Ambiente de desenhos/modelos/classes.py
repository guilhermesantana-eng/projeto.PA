from tkinter import *
from modelos.distancia import distancia
import math

#Classe principal, pai de todas
class Figura:
    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
    
    def desenhar(self, canvas, rascunho=False):
        # MÉTODO EXPLICADO NA ULTIMA AULA DE GIOVANNY
        raise NotImplementedError("As subclasses precisam implementar o método desenhar()")
    
    def mover(self, dx, dy):
        raise NotImplementedError("As subclasses precisam implementar o método mover()")

    def contem_ponto(self, px, py):
        raise NotImplementedError("As subclasses precisam implementar o método contem_ponto()")

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
    
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem_ponto(self, px, py):
        # Verifica se o clique está dentro da caixa delimitadora do retângulo
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        return min_x <= px <= max_x and min_y <= py <= max_y

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
    
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem_ponto(self, px, py):
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        return min_x <= px <= max_x and min_y <= py <= max_y
        
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
    
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem_ponto(self, px, py):
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        return min_x <= px <= max_x and min_y <= py <= max_y

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
    
    def mover(self, dx, dy):
        self.pontos = [(x + dx, y + dy) for x, y in self.pontos]

    def contem_ponto(self, px, py):
        # Checa a distância de (px, py) para cada segmento consecutivo do rabisco
        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i+1]
            if self.distancia(x1, y1, x2, y2, px, py) < 5.0:
                return True
        return False
    
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
    
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem_ponto(self, px, py):
        # AQUI USAMOS A FUNÇÃO DO PROFESSOR (distancia menor que 5 pixels da linha)
        return distancia(self.x1, self.y1, self.x2, self.y2, px, py) < 5.0
    
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

    def mover(self, dx, dy):
        # Percorre os índices modificando X (índices pares) e Y (índices ímpares)
        for i in range(0, len(self.pontos), 2):
            self.pontos[i] += dx      # Altera o X
            self.pontos[i+1] += dy    # Altera o Y
    
    def contem_ponto(self, px, py):
        qtd_coordenadas = len(self.pontos)
        
        # Se não tiver pelo menos 4 números (x1, y1, x2, y2), não é um segmento válido
        if qtd_coordenadas < 4: 
            return False

        # Percorre a lista pulando de 2 em 2 (i assume as posições dos Xs: 0, 2, 4...)
        for i in range(0, qtd_coordenadas, 2):
            x1 = self.pontos[i]
            y1 = self.pontos[i+1]
            
            # Pega o próximo ponto. Se for o último par, conecta de volta ao início do polígono
            if i + 2 < qtd_coordenadas:
                x2 = self.pontos[i+2]
                y2 = self.pontos[i+3]
            else:
                x2 = self.pontos[0]
                y2 = self.pontos[1]

            # Agora chama a função distância (garantindo que ela está fora das classes ou importada)
            if distancia(x1, y1, x2, y2, px, py) < 6.0:
                return True
                
        return False
    
