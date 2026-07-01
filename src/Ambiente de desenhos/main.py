from tkinter import *
from tkinter import colorchooser
from modelos.classes import *

figuras = []                    # GUARDA AS FIGURAS PRONTAS
figura_preview = None           # GUARDA O RASCUNHO QUE APARECE NA HORA EM QUE VOCÊ DESENHA
pontos_poligono = []            # GUARDA AS COORDENADAS PARA O POLIGONO 
linha_poligono = None           # GUARDA O RASCUNHO DO POLIGONO 
linhas_poligono = []            # LINHAS PARA O RASCUNHO DO POLIGONO

x_ini = 0
y_ini = 0

# --- AÇÕES DO MOUSE ---

def iniciarDesenho(event):
    global x_ini, y_ini, figura_preview, pontos_poligono, linhas_poligono, linha_poligono
    x_ini = event.x
    y_ini = event.y

    # RABISCO :
    forma_atual = forma_var.get()
    cor_borda = borda_var.get()
    cor_preenchimento = preencher_var.get()

    if forma_atual == "Rabisco":
       figura_preview = Rabisco(x_ini, y_ini, cor_borda)
    
    elif forma_atual == "Polígono":      #SE FOR POLIGONO, APENAS SALVA OS PONTOS NA LISTA DE PONTOS
        pontos_poligono.append(x_ini)
        pontos_poligono.append(y_ini)

        if len(pontos_poligono) >= 4:
            linha_fixa = canvas.create_line(pontos_poligono[-4], pontos_poligono[-3], pontos_poligono[-2], pontos_poligono[-1])
            linhas_poligono.append(linha_fixa)
        
        linha_poligono = None
        return

def moverDesenho(event):
    # RASCUNHO VISTO NA HORA 
    global figura_preview
    if forma_var.get() == "Polígono":
        return
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

def moverPoligono(event):
    #RASCUNHO DO POLIGONO, POIS TEM UMA FORMA DIFERENTE DE SER DESENHADO
    global linha_poligono, linhas_poligono
    if forma_var.get() != "Polígono":
        return
    else:
        if forma_var.get() == "Polígono" and len(pontos_poligono) >= 2:
            if linha_poligono is not None:    
                canvas.delete(linha_poligono)
            
            x_base = pontos_poligono[-2]
            y_base = pontos_poligono[-1]
            x_atual = event.x
            y_atual = event.y

            linha_poligono = canvas.create_line(x_base, y_base, x_atual, y_atual, dash=(4,2))
            
        else:
            return
    
def terminarDesenho(event):
    global figura_preview, linhas_poligono
    if forma_var.get() == "Polígono":  #CHECAGEM PRA NÃO ATRAPALHAR A CRIAÇÃO DO POLIGONO QUANDO FOR DADO APENAS UM CLICK NO MOUSE
        return
    else:
        if figura_preview:
            # GUARDANDO NA LISTA AS FIGURAS AO SOLTAR O MOUAW
            linhas_poligono = []
            figuras.append(figura_preview)
            figura_preview = None  
            desenhar_tudo()

def terminarPoligono(event):
    global figura_preview, pontos_poligono, linhas_poligono, linha_poligono
    if forma_var.get() == "Polígono":
        #APAGAR O ULTIMO PONTO DUPLICADO POR CONTA DO CLICK DUPLO DO MOUSE, POIS ISSO BUGA A CRIAÇÃO DO POLIGONO
        pontos_poligono.pop()
        pontos_poligono.pop()

        cor_borda = borda_var.get()
        cor_preenchimento = preencher_var.get()

        figura_preview = Poligono(pontos_poligono, cor_borda, cor_preenchimento)

        for linha in linhas_poligono:
            canvas.delete(linha)  #APAGA AS LINHAS DE RASCUNHO

        canvas.delete(linha_poligono)   #APAGA A ULTIMA LINHA
        linha_poligono = None
        linhas_poligono =[]    #LIMPA A LISTA DE LINHAS

        figuras.append(figura_preview) #GUARDANDO O POLIGONO NA LISTA DE FIGURAS E DEPOIS DESENHANDO ELE
        figura_preview = None
        desenhar_tudo()

        pontos_poligono = [] #LIMPANDO A LISTA DE PONTOS PARA FICAR LIMPA PARA O PROXIMO POLIGONO
    else:
        return

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
menu_formas = OptionMenu(funcionalidades, forma_var, "Retângulo", "Oval", "Círculo", "Linha", "Rabisco", "Polígono")
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
canvas.bind("<Double-Button-1>", terminarPoligono)
canvas.bind("<Motion>", moverPoligono)

janela.mainloop()
