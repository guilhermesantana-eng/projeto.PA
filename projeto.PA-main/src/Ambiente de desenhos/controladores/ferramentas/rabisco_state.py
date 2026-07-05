from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import Rabisco

class FerramentaRabisco(FerramentaDesenho):
    def __init__(self):
        self.x_ini = None
        self.y_ini = None

    def iniciar_desenho(self, controller, event):
        self.x_ini = event.x
        self.y_ini = event.y
        cor_borda = controller.view.obter_cor_borda()
        
        controller.desenho.figura_preview = Rabisco(self.x_ini, self.y_ini, cor_borda)

    def mover_desenho(self, controller, event):
        x_atual = event.x
        y_atual = event.y

        if isinstance(controller.desenho.figura_preview, Rabisco):
            controller.desenho.figura_preview.adicionar_pontos(x_atual, y_atual)
        
        controller.desenhar_tudo()

    def terminar_desenho(self, controller, event):
        if controller.desenho.figura_preview:
            controller.desenho.adicionar_figura(controller.desenho.figura_preview)
            controller.desenho.reiniciar_preview()
            controller.desenhar_tudo()