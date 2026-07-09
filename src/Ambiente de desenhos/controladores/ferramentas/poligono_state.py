from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import Poligono

class FerramentaPoligono(FerramentaDesenho):
    def __init__(self):
        self.x_ini = None
        self.y_ini = None
        self.linha_poligono_temp = None
        self.linhas_poligono_fixas_temp = []

    def iniciar_desenho(self, controller, event):
        self.x_ini = event.x
        self.y_ini = event.y

        controller.desenho.adicionar_ponto_poligono(self.x_ini, self.y_ini)

        if len(controller.desenho.pontos_poligono) >= 4:
            linha_fixa = controller.view.canvas.create_line(
                controller.desenho.pontos_poligono[-4], controller.desenho.pontos_poligono[-3],
                controller.desenho.pontos_poligono[-2], controller.desenho.pontos_poligono[-1],
            )
            self.linhas_poligono_fixas_temp.append(linha_fixa)
        

        self.linha_poligono_temp = None

    def mover_desenho(self, controller, event):
        pass

    def mover_poligono(self, controller, event):
        if len(controller.desenho.pontos_poligono) >= 2:
            if self.linha_poligono_temp is not None:
                controller.view.canvas.delete(self.linha_poligono_temp)
            
            x_base = controller.desenho.pontos_poligono[-2]
            y_base = controller.desenho.pontos_poligono[-1]
            x_atual = event.x
            y_atual = event.y

            self.linha_poligono_temp = controller.view.canvas.create_line(
                x_base, y_base, x_atual, y_atual, dash=(4,2)
            )

    def terminar_desenho(self, controller, event):
        pass

    def terminar_poligono(self, controller, event):
        cor_borda = controller.view.obter_cor_borda()
        cor_preench = controller.view.obter_cor_preench()

        controller.desenho.finalizar_poligono(cor_borda, cor_preench)

        for linha in self.linhas_poligono_fixas_temp:
            controller.view.canvas.delete(linha)
        if self.linha_poligono_temp:
            controller.view.canvas.delete(self.linha_poligono_temp)

        self.linha_poligono_temp = None
        self.linhas_poligono_fixas_temp = []

        # Limpa a figura preview para evitar bugs
        controller.desenho.figura_preview = None

        controller.desenhar_tudo()
