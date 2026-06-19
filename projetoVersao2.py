from tkinter import *
from tkinter import colorchooser

# --- MEMÓRIA ---
figuras = []                    # GUARDA AS FIGURAS PRONTAS
figura_preview = None           # GUARDA O RASCUNHO QUE APARECE NA HORA EM QUE VOCÊ DESENHA

x_ini = 0
y_ini = 0

# --- AÇÕES DO MOUSE ---

def iniciarDesenho(event):
    global x_ini, y_ini
    x_ini = event.x
    y_ini = event.y

def moverDesenho(event):
    # RASCUNHO VISTO NA HORA 
    global figura_preview
    x_atual = event.x
    y_atual = event.y
    
    # VALOR ESCOLHIDO MENU
    forma_atual = forma_var.get()
    cor_borda = borda_var.get()
    cor_preenchimento = preencher_var.get()
    
    # P/ O CÍRCULO ACOMPANHAR O MOUSE
    if forma_atual == "Círculo":
        largura = abs(x_atual - x_ini)
        x_atual = x_ini + largura if x_atual > x_ini else x_ini - largura
        y_atual = y_ini + largura if y_atual > y_ini else y_ini - largura

    # OPÇÕES ESCOLHIDAS NO MENU COM RASCUNHO
    figura_preview = (forma_atual, x_ini, y_ini, x_atual, y_atual, cor_borda, cor_preenchimento)
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
    
    # REDESENHA AS FORMAS GUARDADAS NA LISTA
    for fig, x1, y1, x2, y2, cborda, cpreencher in figuras:
        if fig == "Retângulo":
            canvas.create_rectangle(x1, y1, x2, y2, fill=cpreencher, outline=cborda)
        elif fig == "Oval" or fig == "Círculo":
            canvas.create_oval(x1, y1, x2, y2, fill=cpreencher, outline=cborda)
        elif fig == "Linha":
            canvas.create_line(x1, y1, x2, y2, fill = cborda)

    # DESENHA O RASCUNHO ATUAL
    if figura_preview:
        fig, x1, y1, x2, y2, cborda, cpreencher = figura_preview
        if fig == "Retângulo":
            canvas.create_rectangle(x1, y1, x2, y2, fill=cpreencher, outline=cborda, dash=(4, 2))
        elif fig == "Oval" or fig == "Círculo":
            canvas.create_oval(x1, y1, x2, y2, fill = cpreencher, outline=cborda, dash=(4, 2))
        elif fig == "Linha":
            canvas.create_line(x1, y1, x2, y2, fill = cborda, dash=(4,2))

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
menu_formas = OptionMenu(funcionalidades, forma_var, "Retângulo", "Oval", "Círculo", "Linha")
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