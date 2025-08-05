import pygame

pygame.init()

#Configuração Geral

largura_tela = 1366 
altura_tela = 768
screen = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)

#Cores:
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
ciano = (0, 255, 255)
amarelo = (255,255,0)
rosa = (255, 0, 255)
branco = (255, 255, 255)

#Classe coletaveis:
class Coletavel:
    def __init__(self, x, y, tipo):

        self.rect = pygame.Rect(x, y, 30, 30)
        self.tipo = tipo
        self.duracao_efeito = 0

        #analisar qual o tipo do coletavel:
        if (self.tipo == 1):
            self.cor = AZUL
            self.pontos = 5
        
        else:
            
            self.duracao_efeito = 5000

            if (self.tipo == 2):
                self.cor = VERDE
                self.pontos = 0
            
            elif (self.tipo == 3):
                self.cor = CIANO
                self.pontos = 0
        
    #desenhar:
    def desenhar (self, tela):
        pygame.draw.rect (tela, self.cor, self.rect)