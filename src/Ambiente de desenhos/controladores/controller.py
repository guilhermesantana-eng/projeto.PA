from modelos.classes import Retangulo, Oval, Circulo, Linha, Rabisco
from view.view import desenhar_figura_na_tela  # <- Importe a função que criamos para desenhar na View
from controladores.ferramentas.retangulo_state import FerramentaRetangulo
from controladores.ferramentas.circulo_state import FerramentaCirculo
from controladores.ferramentas.oval_state import FerramentaOval
from controladores.ferramentas.linha_state import FerramentaLinha
from controladores.ferramentas.rabisco_state import FerramentaRabisco
from controladores.ferramentas.poligono_state import FerramentaPoligono
from controladores.ferramentas.selecao_state import FerramentaSelecao
from tkinter import filedialog
import copy

class Controlador:
    def __init__(self, view, modelo):
        self.view = view
        self.desenho = modelo
        self.view.controlador = self
        self.estado_atual = None
        self.eh_duplo_clique = False  # Serve para verificar se é um duplo clique

        # Buffer para copiar e colar (Deep Copy)
        self.buffer_copia = [] 

        self.ferramentas = {
            "Retângulo" : FerramentaRetangulo(),
            "Círculo" : FerramentaCirculo(),
            "Oval" : FerramentaOval(),
            "Linha" :  FerramentaLinha(),
            "Rabisco" : FerramentaRabisco(),
            "Polígono" : FerramentaPoligono(),
            "Seleção" : FerramentaSelecao()
        }

        self.ferramenta_atual = self.ferramentas["Retângulo"]
       
        # EVENTOS DO MOUSE
        self.view.canvas.bind("<Button-1>", self.iniciar_desenho)
        self.view.canvas.bind("<B1-Motion>", self.mover_desenho)
        self.view.canvas.bind("<ButtonRelease-1>", self.terminar_desenho)
        self.view.canvas.bind("<Double-Button-1>", self.terminar_poligono)
        self.view.canvas.bind("<Motion>", self.mover_poligono)
        self.view.canvas.bind("<Control-Button-1>", self.selecionar_desenho)
        # EVENTOS DO TECLADO
        self.view.janela.bind("<Delete>", self.excluir_figura)
        self.view.janela.bind("<Control-c>", self.copiar_figura)
        self.view.janela.bind("<Control-v>", self.colar_figura )
        self.view.janela.bind("<Left>", self.alterar_z_index_atras)
        self.view.janela.bind("<Right>", self.alterar_z_index_frente)
        self.view.janela.bind("<Up>", self.alterar_index_todo_frente)
        self.view.janela.bind("<Down>", self.alterar_index_todo_tras)
        self.view.janela.bind("<Control-a>", self.selecionar_tudo)

    def iniciar_desenho(self, event):
        forma_atual = self.view.obter_forma()

        # Se mudar de ferramenta, limpa a seleção direto no Modelo
        if forma_atual != "Seleção":
            self.desenho.figuras_selecionadas.clear()

        self.ferramenta_atual = self.ferramentas[forma_atual]
        self.ferramenta_atual.iniciar_desenho(self, event)
    
    def mover_desenho(self, event):
        self.ferramenta_atual.mover_desenho(self, event)

    def mover_poligono(self, event):
        #RASCUNHO DO POLIGONO, POIS TEM UMA FORMA DIFERENTE DE SER DESENHADO
        self.ferramenta_atual.mover_poligono(self, event)

    def terminar_desenho(self, event):
        self.ferramenta_atual.terminar_desenho(self, event)

    def terminar_poligono(self, event):
        self.eh_duplo_clique = True  # Verifica que é um evento de duplo clique
        self.ferramenta_atual.terminar_poligono(self, event)
    
    def selecionar_desenho(self, event):
        self.ferramenta_atual.selecionar_desenho(self, event)
    
    def selecionar_tudo(self, event):
        self.ferramenta_atual.selecionar_tudo(self, event)

    def desenhar_tudo(self):
        # LIMPA O CANVAS
        self.view.canvas.delete("all")

        # Pega a figura selecionada
        figura_ativa = self.desenho.figuras_selecionadas

        # DESENHA TODAS AS FIGURAS CONCLUÍDAS
        for figura in self.desenho.figuras:
            eh_selecionada = (figura in figura_ativa)
            desenhar_figura_na_tela(self.view.canvas, figura, selecionada=eh_selecionada, rascunho=False)
        
        # DESENHA O RASCUNHO ATUAL, SE HOUVER
        if self.desenho.figura_preview:
            desenhar_figura_na_tela(self.view.canvas, self.desenho.figura_preview, rascunho=True)

    def excluir_figura(self, event):
        if self.desenho.figuras_selecionadas:
            for figura in self.desenho.figuras_selecionadas:
                self.desenho.figuras.remove(figura)
            self.desenho.figuras_selecionadas.clear()
            self.desenhar_tudo()

    def copiar_figura(self, event):
        if self.desenho.figuras_selecionadas:
            self.desenho.buffer_copia = copy.deepcopy(self.desenho.figuras_selecionadas) # ARMAZENA AS FIGURAS NO BUFFER

    def colar_figura(self, event):
        if self.desenho.buffer_copia:
            novas_figuras = copy.deepcopy(self.desenho.buffer_copia)
            for figura in novas_figuras:
                figura.mover(10, 10)         # MOVE A FIGURA COPIADA PARA NÃO SOBREPOR A ORIGINAL
                self.desenho.adicionar_figura(figura)        # ADICIONA A FIGURA COPIADA E COLADA AO DESENHO
            self.desenhar_tudo()

    def salvar_arquivo(self):
        # ABRE A CAIXINHA DE DIÁLOGO PARA SALVAR
        arquivo_path = filedialog.asksaveasfilename(defaultextension=".pkl")
        if arquivo_path:
            self.desenho.salvar_dados(arquivo_path)

    def abrir_arquivo(self):
        # ABRE A CAIXINHA DE DIÁLOGO PARA ABRIR
        arquivo_path = filedialog.askopenfilename(filetypes=[("Arquivos de desenho", "*.pkl")])
        if arquivo_path:
            self.desenho.carregar_dados(arquivo_path)
            self.desenhar_tudo()

    def alterar_z_index_atras(self, event):
       #SETA ESQUERDA- PARA TRÁS
        if self.desenho.figuras_selecionadas:
            for figura in self.desenho.figuras_selecionadas:
                self.desenho.mover_para_tras()
            self.desenhar_tudo()

    def alterar_z_index_frente(self, event):
        #SETA DIREITO- PARA FRENTE
        if self.desenho.figuras_selecionadas:
            for figura in self.desenho.figuras_selecionadas:
                self.desenho.mover_para_frente()
            self.desenhar_tudo()

    def alterar_index_todo_frente(self, event):
        #SETA PARA CIMA
        if self.desenho.figuras_selecionadas:
            for figura in self.desenho.figuras_selecionadas:
                self.desenho.mover_todo_para_frente()
            self.desenhar_tudo()

    def alterar_index_todo_tras(self, event):
        #SETA PARA BAIXO
        if self.desenho.figuras_selecionadas:
            for figura in self.desenho.figuras_selecionadas:
                self.desenho.mover_todo_para_tras()
            self.desenhar_tudo()


    def mudar_cor_figura_selecionada(self, tipo, nova_cor):
        # VÊ SE HÁ ALGUMA FIGURA SELECIONADA
        if self.desenho.figuras_selecionadas:
            for figura in self.desenho.figuras_selecionadas:
                if tipo == 'borda':
                    figura.cor_borda = nova_cor
                elif tipo == 'preenchimento':
                    figura.cor_preenchimento = nova_cor

            # REDESENHA
            self.desenhar_tudo()

    def iniciar(self):
        self.view.janela.mainloop()