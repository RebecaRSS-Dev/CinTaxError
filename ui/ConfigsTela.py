import pygame
from entidades.Player import Player
from niveis.Niveis import Niveis

pygame.init()
class ConfigsTela:
    def __init__(self):

        # Configuração Geral
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.largura_tela, self.altura_tela = self.screen.get_size()

        # Fontes
        self.fonte_pequena = pygame.font.Font('./graphics/fonts/ari-w9500-bold.ttf', 20)
        self.fonte_grande = pygame.font.Font('./graphics/fonts/ari-w9500-bold.ttf', 36)
        
        self.REQUISITOS_FRAGMENTOS = {
            1: 0,  # Sala 1 não precisa de fragmentos para entrar
            2: 1,  # Sala 2 precisa de 1 fragmento
            3: 2,  # Sala 3 precisa de 2 fragmentos
            4: 3   # Sala 4 precisa de 3 fragmentos
        }
        self.player_posicao = Player(0, 0, 40, 40)
        
        self.arquivos_tmx = {
            "Hub": "mapas prontos/entrada.tmx",
            1: "mapas prontos/sala1.tmx",
            2: "mapas prontos/sala2.tmx",
            3: "mapas prontos/sala3.tmx",
            4: "mapas prontos/sala4.tmx"
        }


        self.niveis =  {
        'Hub': Niveis('mapas prontos/entrada.tmx',self.player_posicao, self.largura_tela, self.altura_tela),
        1: Niveis('mapas prontos/sala1.tmx', self.player_posicao, self.largura_tela, self.altura_tela), 
        2: Niveis('mapas prontos/sala2.tmx', self.player_posicao, self.largura_tela, self.altura_tela),
        3: Niveis('mapas prontos/sala3.tmx', self.player_posicao, self.largura_tela, self.altura_tela),
        4: Niveis('mapas prontos/sala4.tmx', self.player_posicao, self.largura_tela, self.altura_tela),
    }
    