import pygame
from Inimigo import Inimigo
from Player import Player
pygame.init()

#Configuração Geral

largura_tela = 1366 
altura_tela = 768
screen = pygame.display.set_mode((largura_tela, altura_tela))

#Cores:
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CIANO = (0, 255, 255)
AMARELO = (255,255,0)
ROSA = (255, 0, 255)
BRANCO = (255, 255, 255)

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

        self.spritesheet = pygame.image.load("New Piskel.png").convert_alpha()
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


background = pygame.transform.scale(pygame.image.load("Background.png").convert(),(largura_tela,altura_tela))
player = Player()

paredes = []

Coletaveis = [Coletavel(50,50,1)]

Inimigos = [Inimigo(700,700,2),Inimigo(300,300,1)]
grupo_inimigos = pygame.sprite.Group()
grupo_inimigos.add(Inimigos)

while True:
    teclasPressionadas = pygame.key.get_pressed()
    player.mover(teclasPressionadas,paredes,Inimigos)
    screen.blit(background, (0, 0))
    player.desenhar(screen)
    Coletaveis[0].update()
    Coletaveis[0].desenhar(screen)

    for inimigo in Inimigos:
        inimigo.move(player,[],Inimigos)
        inimigo.update()
        inimigo.draw(screen)

    for inim in grupo_inimigos:
        pygame.draw.rect(screen, (0, 255, 0), inim.hitbox, 2)
        pygame.draw.rect(screen, (255, 255, 0), inim.rect, 2)  # verde, linha 2 px

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    pygame.display.flip()
    pygame.time.Clock().tick(60)