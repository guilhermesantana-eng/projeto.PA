import math
from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import PoligonoRegular



class FerramentaPoligonoRegular(FerramentaDesenho):
    def __init__(self):
        self.x_centro = None
        self.y_centro = None
        self.vertices  = []
        self.lados = 3
        self.raio = 0
        self.cor_borda = "black"
        self.cor_preench = "white"


    def iniciar_desenho(self, controller, event):
        if self.x_centro is None and self.y_centro is None:
            self.x_centro = event.x
            self.y_centro = event.y
            self.cor_borda = controller.view.obter_cor_borda()

        else:
            if self.lados >= 3: # GARANTIA PRA QUE O MINIMO DE LADOS SEJA 3, POIS UM POLIGONO REGULAR TEM NO MINIMO 3 LADOS
                self.lados += 1
                self.vertices = self.calcular_vertices(self.x_centro, self.y_centro, self.raio, self.lados)
                controller.desenho.figura_preview = PoligonoRegular(self.vertices, self.cor_borda, self.cor_preench)
                controller.desenhar_tudo()
            else:
                self.lados = 3
        
    def diminuir_lados(self, controller, event):
        if self.x_centro is not None and self.y_centro is not None:
            if self.lados > 3:  # SÓ DIMINUI SE TIVER MAIS DE 3 LADOS, NO MINIMO
                self.lados -= 1
                self.vertices = self.calcular_vertices(self.x_centro, self.y_centro, self.raio, self.lados)
                controller.desenho.figura_preview = PoligonoRegular(self.vertices, self.cor_borda, self.cor_preench)
                controller.desenhar_tudo()
            else:
                self.lados = 3

    def mover_poligono(self, controller, event):
        if self.x_centro is not None and self.y_centro is not None:
            self.vertices = []
            x_atual = event.x
            y_atual = event.y
            self.cor_preench = controller.view.obter_cor_preench()
            self.raio = ((x_atual - self.x_centro) ** 2 + (y_atual - self.y_centro) ** 2) ** 0.5

            self.vertices = self.calcular_vertices(self.x_centro, self.y_centro, self.raio, self.lados)

            controller.desenho.figura_preview = PoligonoRegular(self.vertices, self.cor_borda, self.cor_preench)

            controller.desenhar_tudo()

    def terminar_poligono(self, controller, event):
        if controller.desenho.figura_preview:
            self.lados -= 1
            self.vertices = self.calcular_vertices(self.x_centro, self.y_centro, self.raio, self.lados)
            controller.desenho.figura_preview = PoligonoRegular(self.vertices, self.cor_borda, self.cor_preench)
            controller.desenho.adicionar_figura(controller.desenho.figura_preview)
            controller.desenho.reiniciar_preview()
            self.x_centro = None
            self.y_centro = None
            self.vertices = []
            controller.desenhar_tudo()
    
    def calcular_vertices(self, x_centro, y_centro, raio, lados):
        vertices = []
        for i in range(lados):
            angulo = 2 * math.pi * i / lados - math.pi / 2
            x = x_centro + raio * math.cos(angulo)
            y = y_centro + raio * math.sin(angulo)
            vertices.append(x)
            vertices.append(y)
        return vertices