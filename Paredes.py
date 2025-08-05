import pygame # type: ignore
import sys

# Inicialização
pygame.init()
largura, altura = 1280, 760
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Colisão com Paredes")

# Cores
BRANCO = (255, 255, 255)
AZUL = (50, 50, 255)
VERMELHO = (255, 50, 50)
PRETO = (0, 0, 0)

# Clock
relogio = pygame.time.Clock()

class Niveis:
    def __init__(self,fundo_fase1,fundo_fase2,fundo_fase3,coletaveis):
        self.niveis = {
    1: {"fundo": fundo_fase1, "coletaveis": coletaveis([[50, 100, 30, 30],[0,100,30,30]])},
    2: {"fundo": fundo_fase2, "coletaveis": [pygame.Rect(50, 100, 30, 30), pygame.Rect(700, 400, 30, 30)]},
    3: {"fundo": fundo_fase3, "coletaveis": [pygame.Rect(150, 500, 30, 30), pygame.Rect(650, 80, 30, 30)]},
    # Adicione a fase 4 aqui quando tiver
    # 4: {"fundo": fundo_fase4, "coletaveis": [ ... ]
    }
        self.portas = {
        1: pygame.Rect(100, 50, 80, 120),  # Porta da Fase 1 (x, y, largura, altura)
        2: pygame.Rect(300, 50, 80, 120),  # Porta da Fase 2
        3: pygame.Rect(500, 50, 80, 120),  # Porta da Fase 3
        4: pygame.Rect(700, 50, 80, 120)   # Porta da Fase 4
    }




#Coletaveis:
class Coletaveis:
    def __init__(self, objetos:tuple):
        self.pontuacao = 0
        self.coletaveis = []
        for i in range(len(objetos)):
            x,y,larg,alt = objetos[i] 
            self.coletaveis.append(pygame.Rect(x,y,larg,alt))
    def coletar (self, player):
        #logica dos coletaveis:
        for coletavel in self.coletaveis:
            if (player.rect.colliderect(coletavel)):
                self.pontuacao += 1
                self.coletaveis.remove(coletavel)

# Classe Player
class Player:
    def __init__(self):
        self.rect = pygame.Rect(500, 500, 50, 50)
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

# Classe Parede
class Parede:
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, VERMELHO, self.rect)

# Classe Enemy usando sprite com hitbox separada
class Enemy (pygame.sprite.Sprite):
    def __init__(self, x, y,inicial):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))  # controla onde a imagem é desenhada

        # hitbox menor, centralizada na imagem
        hitbox_width, hitbox_height = 50, 150
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center

        self.movimentos = [pygame.Vector2(1,0),pygame.Vector2(0,1),pygame.Vector2(-1,0),pygame.Vector2(0,-1)]
        self.contador = inicial
        self.tempo = pygame.time.get_ticks()
        self.movimento = self.movimentos[self.contador]

    def patrulha(self, paredes,inimigos):
        tempoFinal = pygame.time.get_ticks()
        if (tempoFinal-self.tempo)>=2000:
            self.tempo = tempoFinal
            self.contador += 1
            if self.contador>3:
                self.contador = 0
            self.movimento = self.movimentos[(self.contador)]
        else:
            moviment = self.movimento*2
            newPosition = self.rect.move(moviment)
            newHitbox = self.hitbox.copy()
            newHitbox.center = newPosition.center
            if any(newHitbox.colliderect(p.rect) for p in paredes):
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
                else:
                    print('colisao')

    def perseguir(self,player,paredes):
        selfVector = pygame.Vector2(self.rect.center)
        vetorNormalizedPlayer = pygame.Vector2(player.rect.center)
        moviment = (vetorNormalizedPlayer-selfVector).normalize()
        moviment = moviment*4
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox.copy()
        newHitbox.center = newPosition.center

        if  not any(newHitbox.colliderect(p.rect) for p in paredes) and not newHitbox.colliderect(player.rect):
            self.rect = newPosition


    def move(self,player,paredes,inimigos):
        moviment = pygame.Vector2(0,0)
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox
        if newPosition.colliderect(player.rect):
            self.perseguir(player,paredes)
        elif (not any(newHitbox.colliderect(p.rect) for p in paredes) and
            not newHitbox.colliderect(player.rect)):
            self.patrulha(paredes,inimigos)
        
            
    def update(self):
        # Se mover inimigo, atualize a hitbox também
        self.hitbox.center = self.rect.center

niveis = Niveis("","","",Coletaveis)

# Instanciando jogador e paredes
player = Player()
#coletaveis = Coletaveis()
paredes = [
    Parede(800, 100, 50, 400),
    #Parede(200, 300, 300, 50)
]

inimigos = [Enemy(300,200,0),Enemy(0,200,2)]
grupo_inimigos = pygame.sprite.Group()
grupo_inimigos.add(inimigos)

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    player.mover(teclas, paredes, grupo_inimigos)
    for inimigo in inimigos:
        inimigo.move(player,paredes,inimigos)
    grupo_inimigos.update()
    
    tela.fill(BRANCO)
    grupo_inimigos.draw(tela)
    player.desenhar(tela)

    for parede in paredes:
        parede.desenhar(tela)

    #coletaveis.coletar(player)
    
    #desenhar os coletaveis da fase atual:
    coletaveis = niveis.niveis[1]["coletaveis"]
    for coletavel in coletaveis.coletaveis:
        pygame.draw.rect(tela,(0,255,0), coletavel)
        coletaveis.coletar(player)

    # Opcional: desenhar a hitbox para verificação visual
    for inim in grupo_inimigos:
        pygame.draw.rect(tela, (0, 255, 0), inim.hitbox, 2)
        pygame.draw.rect(tela, (255, 255, 0), inim.rect, 2)  # verde, linha 2 px

    pygame.display.flip()
    relogio.tick(60)
