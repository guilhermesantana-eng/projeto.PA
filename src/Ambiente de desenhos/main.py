import sys
import os
from tkinter import Tk

# -------- ENCONTRAR AS PASTAS DO MODELO SEM DAR MERDA
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.desenho import Desenho
from view.view import View
from controladores.controller import Controlador

def iniciar_app():
    # JANELA RAIZ
    janela = Tk()
    janela.title("Ambiente de Desenhos")
    
    # ABRE MAXIMIZADO
    janela.state('zoomed') 

    # AS TRêS CAMADAS DO MVC
    meu_modelo = Desenho()                           
    minha_visao = View(janela)                       
    meu_controlador = Controlador(minha_visao, meu_modelo)  
    
    # O QUE O BOTAO APAGAR TUDO DEVER FAZER
    minha_visao.BotaoApagar.config(
        command=lambda: [meu_modelo.limpar_todos_os_desenhos(), meu_controlador.desenhar_tudo()]
    )

    janela.mainloop()

if __name__ == "__main__": 
    iniciar_app()