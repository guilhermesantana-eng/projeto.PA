
from tkinter import *
from tkinter import colorchooser


def desenhar_figura_na_tela(canvas, figura, selecionada=False, rascunho=False):
    figura.desenhar(canvas, selecionada, rascunho)

# CLASSE GERAL DO VIEW
class View:
    def __init__(self, janela_principal):
        #---- CRIAR JANELA GERAL E A ABA DE FUNCIONALIDADES
        self.janela = janela_principal
        self.funcionalidades = Frame(janela_principal)
        self.funcionalidades.pack(pady=10)

        #----- CRIAR O BOTÃO DE ESCOLHER FORMA
        Label(self.funcionalidades, text="Escolha a Forma:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
        self.forma_var = StringVar(janela_principal)
        self.forma_var.set("Retângulo")
        self.menu_formas = OptionMenu(self.funcionalidades, self.forma_var, "Retângulo", "Oval", "Círculo", "Linha", "Rabisco", "Polígono", "Seleção")
        self.menu_formas.grid(row=0, column=1, sticky=W, padx=(5,15), pady=5)

        #------ CRIAR BOTAO DE ESCOLHER COR DA BORDA
        Label(self.funcionalidades, text="Cor da Borda:").grid(row=0, column=2, sticky=E, padx=(15,5), pady=5)
        self.borda_var = StringVar(janela_principal)
        self.borda_var.set("black")
        self.BotaoBorda = Button(self.funcionalidades, text = "Selecionar Cor da Borda", command= lambda: self.escolher_cor(self.borda_var))
        self.BotaoBorda.grid(row = 0, column= 3, sticky= W, padx= (5,15), pady= 5)

        #------- CRIAR BOTÃO DE ESCOLHER A COR DE PREENCHIMENTO
        Label(self.funcionalidades, text="Cor de Preenchimento:").grid(row=0, column=4, sticky=E, padx=(15,5), pady=5)
        self.preencher_var = StringVar(janela_principal)
        self.preencher_var.set("white")
        self.BotaoPreench = Button(self.funcionalidades, text = "Selecionar cor do preenchimento", command= lambda: self.escolher_cor(self.preencher_var))
        self.BotaoPreench.grid(row = 0, column= 5, sticky= W, padx= (5,15), pady= 5)

        #-------- CRIAR BOTÃO DE APAGAR
        self.BotaoApagar = Button(self.funcionalidades, text="Apagar Tudo", fg="red")
        self.BotaoApagar.grid(row=0, column=6, sticky=W, padx=15, pady=5)

        #-------- CRIAR O CANVAS
        self.canvas = Canvas(janela_principal, bg="white", width=1920, height=1000)
        self.canvas.pack()

        #-------- CRIAR BOTÃO DE SALVAR
        self.botao_salvar = Button(self.funcionalidades, text="Salvar", command=lambda: self.controlador.salvar_arquivo())
        self.botao_salvar.grid(row=0, column=7, padx=15, pady=5)

        #-------- CRIAR BOTÃO DE ABRIR
        self.botao_abrir = Button(self.funcionalidades, text="Abrir", command=lambda: self.controlador.abrir_arquivo())
        self.botao_abrir.grid(row=0, column=8, padx=15, pady=5)

        #-------- CRIAR BOTÕES DE AGRUPAR/DESAGRUPAR 
        self.botao_agrupar = Button(self.funcionalidades, text="Agrupar (Ctrl+G)", command=lambda: self.controlador.agrupar_figuras())
        self.botao_agrupar.grid(row=1, column=0, columnspan=2, pady=5)

        self.botao_desagrupar = Button(self.funcionalidades, text="Desagrupar (Ctrl+U)", command=lambda: self.controlador.desagrupar_figuras())
        self.botao_desagrupar.grid(row=1, column=2, columnspan=2, pady=5)

    #METODO PRA SELECIONAR AS CORES DE BORDA E PREENCHIMENTO
    def escolher_cor(self, variavel_cor):
        cor_selecionada = colorchooser.askcolor()[1]
        if cor_selecionada:
            variavel_cor.set(cor_selecionada)

            # VÊ SE O BOTÃO CLICADO FOI O DE BORDA OU DE PREENCHIMENTO
            tipo = 'borda' if variavel_cor == self.borda_var else 'preenchimento'

            # CHAMA O MÉTODO "mudar_cor_figura_selecionada"
            if hasattr(self, 'controlador') and self.controlador:
                self.controlador.mudar_cor_figura_selecionada(tipo, cor_selecionada)

    #METODOS PARA OBTER AS VARIAVEIS DE FORMA E CORES
    def obter_forma(self):
        return self.forma_var.get()
    
    def obter_cor_borda(self):
        return self.borda_var.get()
    
    def obter_cor_preench(self):
        return self.preencher_var.get()
    