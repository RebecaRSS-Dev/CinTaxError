import pygame

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

#Classe Inimigos:

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y,inicial):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = pygame.Rect(0, 0, 500, 500)  # rect do tamanho que você quer
        self.rect.center = (x, y)
        #self.rect = pygame.Rect(x,y,100,100)
       # self.rect.center = rect_image.center
        #self.rect.width = 100
        #self.rect.height = 100
        #self.rect = pygame.Rect(x, y, 100, 100)  # cria rect em (0,0) tamanho 100x100
        #self.rect.center = (x,y)  # centraliza o rect na posição desejada


        # hitbox menor, centralizada na imagem
        hitbox_width, hitbox_height = 50, 50
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center

        self.movimentos = [pygame.Vector2(1,0),pygame.Vector2(0,1),pygame.Vector2(-1,0),pygame.Vector2(0,-1)]
        self.contador = inicial
        self.tempo = pygame.time.get_ticks()
        self.movimento = self.movimentos[self.contador]

    def patrulha(self, paredes,inimigos):
        #Lógica do tempo de patrulha
        tempoFinal = pygame.time.get_ticks()
        if (tempoFinal-self.tempo)>=2000:
            self.tempo = tempoFinal
            self.contador += 1
            if self.contador>3:
                self.contador = 0
            self.movimento = self.movimentos[(self.contador)]
        #Se não for hora de mudar direção de movimento
        else:
            moviment = self.movimento*2
            newPosition = self.rect.move(moviment)
            newHitbox = self.hitbox.copy()
            newHitbox.center = newPosition.center
            #Se tocar em parede ou inimigo, 
            if any(newHitbox.colliderect(p.rect) for p in paredes) or any(newHitbox.colliderect(i.hitbox) for i in inimigos if i != self):
                self.contador += 2
                if self.contador>3:
                    self.contador = self.contador - 4
                self.movimento = self.movimentos[(self.contador)]
                moviment = self.movimento*2
                newPosition = self.rect.move(moviment)
                newHitbox = self.hitbox
                self.rect = newPosition
            else:
                if not any(newHitbox.colliderect(i.hitbox) for i in inimigos if i != self):
                    self.rect = newPosition
    def perseguir(self,player,paredes,inimigos):
        #Persegue o player com um vetor que sempre aponta para o centro do sprite
        selfVector = pygame.Vector2(self.rect.center)
        vetorNormalizedPlayer = pygame.Vector2(player.rect.center)
        moviment = (vetorNormalizedPlayer-selfVector).normalize()
        moviment = moviment*4
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox.copy()
        newHitbox.center = newPosition.center

        if  not any(newHitbox.colliderect(p.rect) for p in paredes) and not newHitbox.colliderect(player.rect) and not any(newHitbox.colliderect(i.hitbox) for i in inimigos if i != self):
            self.rect = newPosition


    def move(self,player,paredes,inimigos):
        moviment = pygame.Vector2(0,0)
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox
        if newPosition.colliderect(player.rect):
            self.perseguir(player,paredes,inimigos)
        elif (not any(newHitbox.colliderect(p.rect) for p in paredes) and
            not newHitbox.colliderect(player.rect)):
            self.patrulha(paredes,inimigos)
        
            
    def update(self):
        # Se mover inimigo, atualize a hitbox também
        self.hitbox.center = self.rect.center
    
    def draw(self, surface):
        # Centraliza a imagem dentro do rect do inimigo
        pos_x = self.rect.centerx - self.image.get_width() // 2
        pos_y = self.rect.centery - self.image.get_height() // 2
        surface.blit(self.image, (pos_x, pos_y))


#Classe player
class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.velocidade = 5

    def mover(self, teclas, paredes, inimigos):
        movimento = pygame.Vector2(0, 0)

        if teclas[pygame.K_LEFT]:
            movimento.x = -self.velocidade
        elif teclas[pygame.K_RIGHT]:
            movimento.x = self.velocidade
        if teclas[pygame.K_UP]:
            movimento.y = -self.velocidade
        elif teclas[pygame.K_DOWN]:
            movimento.y = self.velocidade

        if movimento.length() != 0:
            movimento = movimento.normalize() * self.velocidade

        novo_rect = self.rect.move(movimento)
        
        # Verifica colisão com paredes e hitbox dos inimigos
        if (not any(novo_rect.colliderect(p.rect) for p in paredes) and
            not any(novo_rect.colliderect(i.hitbox) for i in inimigos)):
            self.rect = novo_rect

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, AZUL, self.rect)

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
Coletaveis = [Coletavel(50,50,1)]
Inimigos = [Inimigo(700,700,2)]
grupo_inimigos = pygame.sprite.Group()
grupo_inimigos.add(Inimigos)

while True:
    screen.blit(background, (0, 0))
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