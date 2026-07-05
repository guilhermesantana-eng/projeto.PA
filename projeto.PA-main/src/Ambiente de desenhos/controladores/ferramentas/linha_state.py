from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import Linha

class FerramentaLinha(FerramentaDesenho):
    def __init__(self):
        self.x_ini = None
        self.y_ini = None
        self.cor_borda = "black"
        self.cor_preench = "white"
    
    def iniciar_desenho(self, controller, event):
        self.x_ini = event.x
        self.y_ini = event.y
        self.cor_borda = controller.view.obter_cor_borda()
        
    def mover_desenho(self, controller, event):
        x_atual = event.x
        y_atual = event.y
        controller.desenho.figura_preview = Linha(self.x_ini, self.y_ini, x_atual, y_atual, self.cor_borda)

        controller.desenhar_tudo()

    def terminar_desenho(self, controller, event):
        if controller.desenho.figura_preview:
            controller.desenho.adicionar_figura(controller.desenho.figura_preview)
            controller.desenho.reiniciar_preview()
            controller.desenhar_tudo()