from controladores.ferramentas.ferramentaState import FerramentaDesenho
from modelos.classes import *

class FerramentaSelecao(FerramentaDesenho):
    def __init__(self):

        self.x_anterior = 0
        self.y_anterior = 0

    def iniciar_desenho(self, controller, event):
        if controller.eh_duplo_clique:
            self.x_ini = event.x
            self.y_ini = event.y
            self.cor_borda = "grey"
        else:
            self.x_anterior = event.x
            self.y_anterior = event.y

            # Varre as figuras de trás para frente (Z-index: topo primeiro)
            for figura in reversed(controller.desenho.figuras):
                if figura.contem_ponto(event.x, event.y):
                    if figura not in controller.desenho.figuras_selecionadas:
                        controller.desenho.figuras_selecionadas.clear()  # Limpa a seleção anterior
                        controller.desenho.figuras_selecionadas.append(figura)
                        break
            
            controller.desenhar_tudo()

    def mover_desenho(self, controller, event):
        if controller.eh_duplo_clique:
            x_atual = event.x
            y_atual = event.y
            self.cor_preench = None
            controller.desenho.figura_preview = Retangulo(self.x_ini, self.y_ini, x_atual, y_atual, self.cor_borda, self.cor_preench)
            
            controller.desenhar_tudo()
        else:
            if controller.desenho.figuras_selecionadas:
                dx = event.x - self.x_anterior
                dy = event.y - self.y_anterior
                
                # Aplica o movimento no modelo
                for figura in controller.desenho.figuras_selecionadas:
                    figura.mover(dx, dy)
                
                self.x_anterior = event.x
                self.y_anterior = event.y
                controller.desenhar_tudo()
    
    def terminar_desenho(self, controller, event):
        if controller.eh_duplo_clique:
            if controller.desenho.figura_preview:
                for figura in reversed(controller.desenho.figuras):
                    if figura.esta_dentro(controller.desenho.figura_preview.x1, controller.desenho.figura_preview.y1, controller.desenho.figura_preview.x2, controller.desenho.figura_preview.y2):
                        if figura not in controller.desenho.figuras_selecionadas:
                            controller.desenho.figuras_selecionadas.append(figura)
                controller.view.canvas.delete("preview")  # Remove o retângulo de seleção da tela
                controller.eh_duplo_clique = False  # Reseta a flag após o evento
                controller.desenho.reiniciar_preview()
                controller.desenhar_tudo()

    def selecionar_desenho(self, controller, event):
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

    def terminar_poligono(self, controller, event):
        if controller.eh_duplo_clique:
            self.x_ini = event.x
            self.y_ini = event.y
            self.cor_borda = "grey"
    
    def selecionar_tudo(self, controller, event):
        if controller.desenho.figuras_selecionadas != controller.desenho.figuras:
            controller.desenho.figuras_selecionadas = controller.desenho.figuras.copy()
            controller.desenhar_tudo()
        else:
            controller.desenho.figuras_selecionadas.clear()
            controller.desenhar_tudo()