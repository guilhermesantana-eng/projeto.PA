from modelos.classes import Poligono
import pickle


class Desenho:
    def __init__(self):
        # ARMAZENAMENTO E VARIÁVEIS GLOBAIS
        self.figuras = []                    # GUARDA OS PONTOS
        self.figura_preview = None           # GUARDA O RASCUNHO ATUAL
        self.pontos_poligono = []            # GUARDA AS COORDENADAS ATUAIS DO POLÍGONO
        self.figura_selecionada = None       # GUARDA A FIGURA SELECIONADA (SE HOUVER)
        self.buffer_copia = None             # BUFFER PRA GUARDAR A FIGURA COPIADA

    def adicionar_figura(self, figura):
        # --- ADICIONA UMA FIGURA CONCLUÍDA NA LISTA GLOBAL
        self.figuras.append(figura)
        
    def limpar_todos_os_desenhos(self):
        # --- APAGAR TUDO
        self.figuras.clear()
        self.figura_preview = None
        self.pontos_poligono.clear()

    def reiniciar_preview(self):
        # --- RESETA O RASCUNHO
        self.figura_preview = None

    def adicionar_ponto_poligono(self, x, y):
        # GUARDA OS PONTOS DOIS POLÍGONOS (TEMPORARIAMENTE)
        self.pontos_poligono.append(x)
        self.pontos_poligono.append(y)

    def finalizar_poligono(self, cor_borda, cor_preenchimento):
        # GERA O POLÍGONO E APAGA O TEMPORÁRIO
        if len(self.pontos_poligono) >= 4:
            # REMOVE OS PONTOS DUPLICADOS
            self.pontos_poligono.pop()
            self.pontos_poligono.pop()
            
        # CRIA O POLÍGONO PASSANDO UMA CÓPIA SEGURA DA LISTA DE PONTOS
        novo_poligono = Poligono(self.pontos_poligono.copy(), cor_borda, cor_preenchimento)
        
        # LIMPA OS PONTOS TEMPORÁRIOS PARA O PRX POLÍGONO
        self.pontos_poligono.clear()
        
        # aqui já adiciona direto ao array do armazenamento
        self.adicionar_figura(novo_poligono)
        return novo_poligono
    
    def salvar_dados(self, nome_arquivo):
        # ABRE O ARQUIVO 
        arquivo = open(nome_arquivo, "wb")
        pickle.dump(self.figuras, arquivo)
        arquivo.close()
    
    def carregar_dados(self, nome_arquivo):
        #ABRE O ARQUIVO EM MODO DE LEITURA BINÁRIA
        arquivo = open(nome_arquivo, 'rb')
        dados_carregados = pickle.load(arquivo)
        self.figuras.clear()
        self.figuras.extend(dados_carregados)
        
        # FECHA APÓS LER
        arquivo.close()
