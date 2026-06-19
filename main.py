from tkinter import *

#Variaveis Globais, para o formato do desenho, cores
ferramenta_atual = "nenhuma"
corBorda_atual = "black"
corPreencher_atual = "white"

#Estrutura para desenhar
x_ini = 0
y_ini = 0

def iniciarDesenho(event):
    global x_ini, y_ini
    x_ini = event.x
    y_ini = event.y

def terminarDesenho(event):
    x_final = event.x
    y_final = event.y
    
    #canvas.delete("all") => não sei se é pra apagar ou não, então deixei comentado 
    if ferramenta_atual == "Retangulo":
        canvas.create_rectangle(x_ini, y_ini, x_final, y_final, fill=corPreencher_atual, outline=corBorda_atual)
    elif ferramenta_atual == "Oval":
        canvas.create_oval(x_ini, y_ini, x_final, y_final, fill=corPreencher_atual, outline=corBorda_atual)
    elif ferramenta_atual == "Circulo":
        largura = abs(x_final - x_ini)
        y_final = y_ini + largura
        canvas.create_oval(x_ini, y_ini, x_final, y_final, fill=corPreencher_atual, outline=corBorda_atual)


#Funções para selecionar qual o formato do desenho
def ativarRetangulo():
    global ferramenta_atual
    ferramenta_atual = "Retangulo"

def ativarOval():
    global ferramenta_atual
    ferramenta_atual = "Oval"

def ativarCirculo():
    global ferramenta_atual
    ferramenta_atual = "Circulo"

def atualizarCores():
    global corBorda_atual, corPreencher_atual
    corBorda_atual = cor_borda.get()
    corPreencher_atual = cor_preencher.get()


#Criando Janela e o frame para os botões
janela = Tk()
janela.title("Ambiente de Desenhos")
funcionalidades = Frame(janela)
funcionalidades.pack()

#Botôes para cada funcionalidade e para escolher as cores
butao_retangulo = Button(funcionalidades, text="Retângulo", command=ativarRetangulo)
butao_retangulo.grid( row=0, column=0)
butao_oval = Button(funcionalidades, text="Oval", command=ativarOval)
butao_oval.grid(row=0, column=1)
butao_circulo = Button(funcionalidades, text="Circulo", command=ativarCirculo)
butao_circulo.grid( row=0, column=2)

corBorda = Label(funcionalidades, text="Cor da Borda:")
corBorda.grid(row=1, column=0)
cor_borda = Entry(funcionalidades)
cor_borda.grid(row=1, column=1)
corPreencher = Label(funcionalidades, text="Cor de Preenchimento:")
corPreencher.grid(row=2, column=0)
cor_preencher = Entry(funcionalidades)
cor_preencher.grid(row=2, column=1)

botao_cores = Button(funcionalidades, text="Aplicar Cores", command=atualizarCores)
botao_cores.grid(row=2,column=2)

#Criando o canva e recebendo os clicks do mouse
canvas = Canvas(janela, bg="white", width=600, height=600)
canvas.pack()
canvas.bind("<Button-1>", iniciarDesenho)
canvas.bind("<ButtonRelease-1>", terminarDesenho)

janela.mainloop()