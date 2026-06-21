from tkinter import *
from tkinter import colorchooser

class Figura:
    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
    
    def desenhar(self, canvas, rascunho=False):
        # MÉTODO EXPLICADO NA ULTIMA AULA DE GIOVANNY
        raise NotImplementedError("As subclasses precisam implementar o método desenhar()")
    
class Retangulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline = self.cor_borda,
            fill = self.cor_preenchimento, 
            dash = estilo_rascunho
        )

class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            fill = self.cor_preenchimento, 
            outline = self.cor_borda, 
            dash = estilo_rascunho)
        
class Circulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        largura = abs(self.x1 - self.x2)
        self.x2 = self.x1 + largura if self.x2 > self.x1 else self.x1 - largura
        self.y2 = self.y1 + largura if self.y2 > self.y1 else self.y1 - largura

    
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4,2) if rascunho else None

        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2, 
            fill = self.cor_preenchimento, 
            outline = self.cor_borda, 
            dash = estilo_rascunho
        )

class Rabisco(Figura):
    def __init__(self, x1, y1, cor_borda):
        super().__init__(cor_borda, cor_preenchimento = None)
        self.pontos = [(x1, y1)]
    
    def adicionar_pontos(self, x, y):
        #MÉTODO PARA O RABISCO ACUMULAR O RASTRO DEIXAD PELO MOUSE
        self.pontos.append((x, y))

    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4, 2) if rascunho else None

        if len(self.pontos) > 1:
            canvas.create_line(
                self.pontos, 
                fill=self.cor_borda, 
                dash=estilo_rascunho
            )

class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda):
        super().__init__(cor_borda, cor_preenchimento = None)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def desenhar(self, canvas, rascunho = False):
        estilo_rascunho = (4, 2) if rascunho else None

        canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                           fill = self.cor_borda,
                           dash = estilo_rascunho)

# --- MEMÓRIA ---
figuras = []                    # GUARDA AS FIGURAS PRONTAS
figura_preview = None           # GUARDA O RASCUNHO QUE APARECE NA HORA EM QUE VOCÊ DESENHA

x_ini = 0
y_ini = 0

# --- AÇÕES DO MOUSE ---

def iniciarDesenho(event):
    global x_ini, y_ini, figura_preview
    x_ini = event.x
    y_ini = event.y

    # RABISCO :
    forma_atual = forma_var.get()
    cor_borda = borda_var.get()
    cor_preenchimento = preencher_var.get()

    if forma_atual == "Rabisco":
       figura_preview = Rabisco(x_ini, y_ini, cor_borda)

def moverDesenho(event):
    # RASCUNHO VISTO NA HORA 
    global figura_preview
    x_atual = event.x
    y_atual = event.y
    
    # VALOR ESCOLHIDO MENU
    forma_atual = forma_var.get()
    cor_borda = borda_var.get()
    cor_preenchimento = preencher_var.get()
    
    # RABISCO SE ADICIONA APENAS O PONTO AO OBJETO
    if forma_atual == "Rabisco":
        if isinstance(figura_preview, Rabisco):
            figura_preview.adicionar_pontos(x_atual, y_atual)
    
    else: 
        if forma_atual == "Retângulo":
            figura_preview = Retangulo(x_ini, y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
        elif forma_atual == "Oval":
            figura_preview = Oval(x_ini, y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
        elif forma_atual == "Círculo":
            figura_preview = Circulo(x_ini, y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
        elif forma_atual == "Linha":
            figura_preview = Linha(x_ini, y_ini, x_atual, y_atual, cor_borda)

    desenhar_tudo()

def terminarDesenho(event):
    global figura_preview
    if figura_preview:
        # GUARDANDO NA LISTA AS FIGURAS AO SOLTAR O MOUAW
        figuras.append(figura_preview)
        figura_preview = None  
        desenhar_tudo()

# --- RECONSTRUÇÃO VISUAL ---

def desenhar_tudo():
    canvas.delete("all")  
    
    # REDESENHA AS FORMAS 
    for figura in figuras:
        figura.desenhar(canvas)
            
    # DESENHA O RASCUNHO ATUAL
    if figura_preview:
        figura_preview.desenhar(canvas, rascunho=True)


def escolher_cor(variavel_tk):
    cor_selecionada = colorchooser.askcolor()[1]
    if cor_selecionada:
        variavel_tk.set(cor_selecionada)
    
def deletar():
    global figuras
    figuras.clear()  
    desenhar_tudo()
    


# --- JANELA E O FRAME P/ BOTÕES ---
janela = Tk()
janela.title("Ambiente de Desenhos")
funcionalidades = Frame(janela)
funcionalidades.pack(pady=10)

# --- MENU DE FORMAS ---
Label(funcionalidades, text="Escolha a Forma:").grid(row=0, column=0, sticky=E, padx=5, pady=5)

forma_var = StringVar(janela)
forma_var.set("Retângulo")  # opção inicial
menu_formas = OptionMenu(funcionalidades, forma_var, "Retângulo", "Oval", "Círculo", "Linha", "Rabisco")
menu_formas.grid(row=0, column=1, sticky=W, padx=(5,15), pady=5)


# --- MENU DA COR DA BORDA ---
Label(funcionalidades, text="Cor da Borda:").grid(row=0, column=2, sticky=E, padx=(15,5), pady=5)

borda_var = StringVar(janela)
borda_var.set("black")      # cor inicial 

# BOTÃO PARA COR
botaoBorda = Button(funcionalidades, text = "Selecionar Cor da Borda", command= lambda: escolher_cor(borda_var))
botaoBorda.grid(row = 0, column= 3, sticky= W, padx= (5,15), pady= 5)

# --- MNENU DA COR DE PREENCHIMENTO ---
Label(funcionalidades, text="Cor de Preenchimento:").grid(row=0, column=4, sticky=E, padx=(15,5), pady=5)

preencher_var = StringVar(janela)
preencher_var.set("white")  # cor inicial

# BOTÃO PARA COR
botaoPreench = Button(funcionalidades, text = "Selecionar cor do preenchimento", command= lambda: escolher_cor(preencher_var))
botaoPreench.grid(row = 0, column= 5, sticky= W, padx= (5,15), pady= 5)

# --- BOTÃO DE APAGAR TUDO ---
botaoApagar = Button(funcionalidades, text="Apagar Tudo", command= deletar, fg="red") 
botaoApagar.grid(row=0, column=6, sticky=W, padx=15, pady=5)


# --- CANVAS  ---
canvas = Canvas(janela, bg="white", width=1920, height=1000)
canvas.pack()

# eventos do mouse
canvas.bind("<Button-1>", iniciarDesenho)
canvas.bind("<B1-Motion>", moverDesenho)
canvas.bind("<ButtonRelease-1>", terminarDesenho)

janela.mainloop()
