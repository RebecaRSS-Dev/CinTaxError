import pygame
from graphics.Cores import Cores

class Coletavel:
    def __init__(self, x, y, tipo):
        super().__init__()
        self.rect = pygame.Rect(x, y, 30, 30)
        self.tipo = tipo
        self.duracao_efeito = 0
        self.fragmentos = 0
        self.is_animated = False 

        # Analisar qual o tipo do coletavel:
        if self.tipo == 1:
            self.is_animated = True 
            self.cor = Cores.AZUL
            self.pontos = 5
            
            # Carrega a spritesheet e configura a animação
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

        else:
            # --- LÓGICA PARA OS COLETÁVEIS ESTÁTICOS (SEM ANIMAÇÃO) ---
            self.duracao_efeito = 5000
            
            if self.tipo == 2:
                self.cor = Cores.VERDE
                self.pontos = 1
                # Carrega a imagem estática específica para o tipo 2
                self.image = pygame.image.load("./imagens/Sprites/Shield.png").convert_alpha()
            
            elif self.tipo == 3:
                self.cor = Cores.CIANO
                self.pontos = 1
                # Carrega a imagem estática específica para o tipo 3
                self.image = pygame.image.load("./imagens/Sprites/Speed.png").convert_alpha()
            
            elif self.tipo == 4:
                self.cor = Cores.AMARELO
                self.pontos = 0
                # Carrega a imagem estática específica para o tipo 4
                self.imagem_fragmentos = []
                #organizar todas as imagens de fragmentos:
                for i in range (1, 5):
                    imagem = pygame.image.load(f"./imagens/Sprites/Fragmento {i}.png").convert_alpha()
                    imagem = pygame.transform.scale(imagem, (self.rect.width, self.rect.height))
                    self.imagem_fragmentos.append(imagem)
                
                self.image = self.imagem_fragmentos[0]  # Usa o primeiro fragmento como imagem inicial
            
            # Redimensiona a imagem para o tamanho do rect, se necessário
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def load_frames(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.spritesheet.subsurface((x, y, self.frame_width, self.frame_height))
                frames.append(frame)
        return frames

    def update(self, fragmentos_do_player = 0):
        # Atualiza a animação se o coletável for animado
        if self.is_animated:
            self.frame_timer += self.animation_speed
            if self.frame_timer >= 1:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        
        elif self.tipo == 4:
            #impedir que pegue um indice que não existe:
            indicie_imagem = min(fragmentos_do_player, len(self.imagem_fragmentos) - 1)
            self.image = self.imagem_fragmentos[indicie_imagem]
    
    #desenhar:
    def desenhar (self, tela):
        tela.blit(self.image, self.rect.topleft)