from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import *

class FerramentaSelecao(FerramentaDesenho):
    def __init__(self):

        self.x_anterior = 0
        self.y_anterior = 0

    def iniciar_desenho(self, controller, event):
        self.x_anterior = event.x
        self.y_anterior = event.y

        # Varre as figuras de trás para frente (Z-index: topo primeiro)
        for figura in reversed(controller.desenho.figuras):
            if figura.contem_ponto(event.x, event.y):
                if figura not in controller.desenho.figuras_selecionadas:
                    controller.desenho.figuras_selecionadas.append(figura)
                    break
                else:
                    controller.desenho.figuras_selecionadas.remove(figura)
                    break
        
        controller.desenhar_tudo()

    def mover_desenho(self, controller, event):
        if controller.desenho.figuras_selecionadas:
            dx = event.x - self.x_anterior
            dy = event.y - self.y_anterior
            
            # Aplica o movimento no modelo
            for figura in controller.desenho.figuras_selecionadas:
                figura.mover(dx, dy)
            
            self.x_anterior = event.x
            self.y_anterior = event.y
            controller.desenhar_tudo()