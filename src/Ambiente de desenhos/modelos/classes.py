from tkinter import *
from modelos.distancia import distancia
import math

#Classe principal, pai de todas
class Figura:
    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
    
    # Refatorado para aceitar a flag de seleção de forma independente
    def desenhar(self, canvas, selecionada=False, rascunho=False):
        # MÉTODO EXPLICADO NA ULTIMA AULA DE GIOVANNY
        raise NotImplementedError("As subclasses precisam implementar o método desenhar()")
    
    def mover(self, dx, dy):
        raise NotImplementedError("As subclasses precisam implementar o método mover()")

    def contem_ponto(self, px, py):
        raise NotImplementedError("As subclasses precisam implementar o método contem_ponto()")
    
    def esta_dentro(self, x, y):
        raise NotImplementedError("As subclasses precisam implementar o método esta_dentro()")
    
#Subclasses 
class Retangulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas, selecionada = False, rascunho = False):
        cor_borda_atual = "green" if selecionada else self.cor_borda
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline = cor_borda_atual,
            fill = self.cor_preenchimento, 
            dash = estilo_rascunho,
            width = 5
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
    
    def esta_dentro(self, x1, y1, x2, y2):
        # Verifica se o retângulo está completamente dentro da área definida por (x1, y1) e (x2, y2)
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        return (min_x <= self.x1 <= max_x and min_y <= self.y1 <= max_y and
                min_x <= self.x2 <= max_x and min_y <= self.y2 <= max_y)

class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, canvas, selecionada = False, rascunho = False):
        cor_borda_atual = "green" if selecionada else self.cor_borda
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            fill = self.cor_preenchimento, 
            outline = cor_borda_atual, 
            dash = estilo_rascunho,
            width = 5
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
    
    def esta_dentro(self, x1, y1, x2, y2):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        return (min_x <= self.x1 <= max_x and min_y <= self.y1 <= max_y and
                min_x <= self.x2 <= max_x and min_y <= self.y2 <= max_y)
        
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

    def desenhar(self, canvas, selecionada = False, rascunho = False):
        cor_borda_atual = "green" if selecionada else self.cor_borda
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            fill = self.cor_preenchimento, 
            outline = cor_borda_atual, 
            dash = estilo_rascunho,
            width = 5
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
    
    def esta_dentro(self, x1, y1, x2, y2):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        return (min_x <= self.x1 <= max_x and min_y <= self.y1 <= max_y and
                min_x <= self.x2 <= max_x and min_y <= self.y2 <= max_y)

class Rabisco(Figura):
    def __init__(self, x1, y1, cor_borda):
        super().__init__(cor_borda, cor_preenchimento = None)
        self.pontos = [(x1, y1)]
    
    def adicionar_pontos(self, x, y):
        #MÉTODO PARA O RABISCO ACUMULAR O RASTRO DEIXADO PELO MOUSE
        self.pontos.append((x, y))

    def desenhar(self, canvas, selecionada = False, rascunho = False):
        cor_borda_atual = "green" if selecionada else self.cor_borda
        estilo_rascunho = (4, 2) if rascunho else None

        if len(self.pontos) > 1:
            canvas.create_line(
                self.pontos, 
                fill = cor_borda_atual, 
                dash = estilo_rascunho,
                width = 5
            )
    
    def mover(self, dx, dy):
        self.pontos = [(x + dx, y + dy) for x, y in self.pontos]

    def contem_ponto(self, px, py):
        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i+1]
            if distancia(x1, y1, x2, y2, px, py) < 5.0:
                return True
        return False
    
    def esta_dentro(self, x1, y1, x2, y2):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        for px, py in self.pontos:
            if not (min_x <= px <= max_x and min_y <= py <= max_y):
                return False
        return True
    
class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda):
        super().__init__(cor_borda, cor_preenchimento = None)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, canvas, selecionada = False, rascunho = False):
        cor_borda_atual = "green" if selecionada else self.cor_borda
        estilo_rascunho = (4, 2) if rascunho else None

        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill = cor_borda_atual,
            dash = estilo_rascunho,
            width = 5
        )
    
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def contem_ponto(self, px, py):
        # AQUI USAMOS A FUNÇÃO DO PROFESSOR (distancia menor que 5 pixels da linha)
        return distancia(self.x1, self.y1, self.x2, self.y2, px, py) < 5.0
    
    def esta_dentro(self, x1, y1, x2, y2):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        return (min_x <= self.x1 <= max_x and min_y <= self.y1 <= max_y and
                min_x <= self.x2 <= max_x and min_y <= self.y2 <= max_y)
    
class Poligono(Figura):
    def __init__(self, pontos, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.pontos = pontos
        
    def desenhar(self, canvas, selecionada = False, rascunho = False):
        cor_borda_atual = "green" if selecionada else self.cor_borda
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_polygon(
            self.pontos,
            fill = self.cor_preenchimento,
            outline = cor_borda_atual,
            dash = estilo_rascunho,
            width = 5
        )

    def mover(self, dx, dy):
        # Percorre os índices modificando X (índices pares) e Y (índices ímpares)
        for i in range(0, len(self.pontos), 2):
            self.pontos[i] += dx      # Altera o X
            self.pontos[i+1] += dy    # Altera o Y
    
    def contem_ponto(self, px, py):
        """
        Versão adaptada do algoritmo do professor para lista linear [x1, y1, x2, y2...].
        Garante o clique no centro/preenchimento do polígono sem alterar o Modelo.
        """
        dentro = False
        qtd_coordenadas = len(self.pontos)
        
        # Como cada ponto ocupa 2 posições (x e y), a quantidade de vértices é total / 2
        n_vertices = qtd_coordenadas // 2

        # Um polígono válido precisa de pelo menos 3 vértices (6 coordenadas)
        if n_vertices < 3:
            return False

        # Inicializa o primeiro vértice (índice 0 e 1) como ponto de partida
        p1x = self.pontos[0]
        p1y = self.pontos[1]

        # O laço roda para cada vértice (e faz uma volta extra para fechar o polígono)
        for i in range(n_vertices + 1):
            # Descobre o índice real na lista linear usando o resto da divisão (%)
            # i % n_vertices garante que na última volta ele conecte ao primeiro vértice de novo
            indice_base = (i % n_vertices) * 2
            
            p2x = self.pontos[indice_base]
            p2y = self.pontos[indice_base + 1]

            # --- Daqui para baixo é a lógica matemática exata do professor ---
            # Verifica se o raio horizontal intercepta a aresta do polígono
            if py > min(p1y, p2y):
                if py <= max(p1y, p2y):
                    if px <= max(p1x, p2x):
                        # Calcula a interceptação X exata da aresta
                        if p1y != p2y:
                            x_interceptado = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # Se o ponto estiver à esquerda da interceptação, inverte o estado
                        if p1x == p2x or px <= x_interceptado:
                            dentro = not dentro

            # O próximo ponto de partida (p1) passa a ser o ponto de chegada atual (p2)
            p1x, p1y = p2x, p2y

        return dentro
    
    def esta_dentro(self, x1, y1, x2, y2):
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        for i in range(0, len(self.pontos), 2):
            px = self.pontos[i]
            py = self.pontos[i + 1]
            if not (min_x <= px <= max_x and min_y <= py <= max_y):
                return False
        return True

class FiguraComposta(Figura):
    def __init__(self, figuras):
        self.figuras = figuras
        self._cor_borda = None
        self._cor_preenchimento = None

    # --- COR DA BORDA
    @property
    def cor_borda(self):
        return self._cor_borda

    @cor_borda.setter
    def cor_borda(self, nova_cor):
        self._cor_borda = nova_cor
        # REPASSA A COR DA BORDA PARA TODAS AS FIGURAS
        for figura in self.figuras:
            figura.cor_borda = nova_cor

    # --- COR DE PREENCHIMENTO
    @property
    def cor_preenchimento(self):
        return self._cor_preenchimento

    @cor_preenchimento.setter
    def cor_preenchimento(self, nova_cor):
        self._cor_preenchimento = nova_cor
        # REPASSA A COR DO PREENCHIMENTO PARA TODAS AS FIGURAS
        for figura in self.figuras:
            figura.cor_preenchimento = nova_cor

    def desenhar(self, canvas, selecionada=False, rascunho=False):
        for figura in self.figuras:
            figura.desenhar(canvas, selecionada, rascunho)
    
    def mover(self, dx, dy):
        for figura in self.figuras:
            figura.mover(dx, dy)

    def contem_ponto(self, px, py):
        for figura in self.figuras:
            if figura.contem_ponto(px, py):
                return True
        return False
    
    def esta_dentro(self, x1, y1, x2, y2):
        for figura in self.figuras:
            if not figura.esta_dentro(x1, y1, x2, y2):
                return False
        return True