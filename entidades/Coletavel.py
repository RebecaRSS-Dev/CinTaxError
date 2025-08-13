import pygame
from graphics.Cores import Cores

class Coletavel:
    def __init__(self, x, y, tipo):
        super().__init__()
        self.rect = pygame.Rect(x, y, 30, 30)
        self.tipo = tipo
        self.duracao_efeito = 0
        self.fragmentos = 0
        #analisar qual o tipo do coletavel:
        if self.tipo == 1:
            self.cor = Cores.AZUL
            self.pontos = 5
        else:
            self.duracao_efeito = 5000
            if self.tipo == 2:
                self.cor = Cores.VERDE
                self.pontos = 1
            elif self.tipo == 3:
                self.cor = Cores.CIANO
                self.pontos = 1
            elif self.tipo == 4:
                self.cor = Cores.AMARELO
                self.pontos = 0
        self.spritesheet = pygame.image.load("./imagens/Sprites/New Piskel.png").convert_alpha()
        self.frame_width = 32
        self.frame_height = 32
        self.columns = 3
        self.rows = 4
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

    def load_frames(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.spritesheet.subsurface((x, y, self.frame_width, self.frame_height))
                frames.append(frame)
        return frames

    def update(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    #desenhar:
    def desenhar (self, tela):
        tela.blit(self.image, self.rect.topleft)