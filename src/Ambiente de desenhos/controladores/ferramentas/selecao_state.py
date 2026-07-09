from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import *

class FerramentaSelecao(FerramentaDesenho):
    def __init__(self):

        self.x_anterior = 0
        self.y_anterior = 0

    def iniciar_desenho(self, controller, event):
        self.x_anterior = event.x
        self.y_anterior = event.y
        controller.desenho.figura_selecionada = None

        # Varre as figuras de trás para frente (Z-index: topo primeiro)
        for figura in reversed(controller.desenho.figuras):
            if figura.contem_ponto(event.x, event.y):
                controller.desenho.figura_selecionada = figura
                break
        
        controller.desenhar_tudo()

    def mover_desenho(self, controller, event):
        if controller.desenho.figura_selecionada:
            dx = event.x - self.x_anterior
            dy = event.y - self.y_anterior
            
            # Aplica o movimento no modelo
            controller.desenho.figura_selecionada.mover(dx, dy)
            
            self.x_anterior = event.x
            self.y_anterior = event.y
            controller.desenhar_tudo()