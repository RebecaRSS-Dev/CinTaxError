import pygame
import sys

# Inicialização
pygame.init()
largura, altura = 1366, 760
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Colisão com Paredes")

# Cores
BRANCO = (255, 255, 255)
AZUL = (50, 50, 255)
VERMELHO = (255, 50, 50)
PRETO = (0, 0, 0)

# Clock
relogio = pygame.time.Clock()

# Classe Player
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)
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
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))  # controla onde a imagem é desenhada

        # hitbox menor, centralizada na imagem
        hitbox_width, hitbox_height = 50, 150
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center
    
    def perseguir(self,player):
        selfVector = pygame.Vector2(self.rect.center)
        vetorNormalizedPlayer = pygame.Vector2(player.rect.center)
        moviment = (vetorNormalizedPlayer-selfVector).normalize()
        moviment = moviment*4
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox.copy()
        newHitbox.center = newPosition.center

        if not newHitbox.colliderect(player.rect):
            self.rect = newPosition


    def move(self,player):
        moviment = pygame.Vector2(0,0)
        moviment.x = 2
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox
        if newPosition.colliderect(player.rect):
            self.perseguir(player)
        elif (not any(newPosition.colliderect(p.rect) for p in paredes) and
            not newHitbox.colliderect(player.rect)):
            self.rect = newPosition
        
            
    def update(self):
        # Se mover inimigo, atualize a hitbox também
        self.hitbox.center = self.rect.center

# Instanciando jogador e paredes
player = Player()
paredes = [
    # Parede(300, 100, 50, 400),
    # Parede(200, 300, 300, 50)
]

inimigo = Enemy(300, 100)
grupo_inimigos = pygame.sprite.Group()
grupo_inimigos.add(inimigo)

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    player.mover(teclas, paredes, grupo_inimigos)
    inimigo.move(player)

    tela.fill(BRANCO)
    player.desenhar(tela)

    for parede in paredes:
        parede.desenhar(tela)
    
    grupo_inimigos.update()
    grupo_inimigos.draw(tela)

    # Opcional: desenhar a hitbox para verificação visual
    for inim in grupo_inimigos:
        pygame.draw.rect(tela, (0, 255, 0), inim.hitbox, 2)
        pygame.draw.rect(tela, (255, 255, 0), inim.rect, 2)  # verde, linha 2 px

    pygame.display.flip()
    relogio.tick(60)
