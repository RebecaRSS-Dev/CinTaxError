import pygame

pygame.init()

LARGURA = 800
ALTURA = 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Byte Game")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

byte_height = 800 * 0.20
byte_width = byte_height * 0.40

byte_img = pygame.image.load("./front_byte1.1.png")
byte_img = pygame.transform.scale(byte_img, (byte_width // 2, byte_height // 2))
byte_width, byte_height = byte_img.get_size()

byte_x = 50
byte_y = ALTURA - byte_height - 10

velocidade = 5

obstaculos = [
    pygame.Rect(200, 50, 20,100),
    pygame.Rect(400, 0, 20, 100),
    pygame.Rect(300, 150, 20, 100),
    pygame.Rect(300, 200, 200, 20)
]

colisoes = 0
clock = pygame.time.Clock()
executando = True
itens = [
    pygame.Rect(100, 300, 20, 20),
    pygame.Rect(600, 350, 20, 20),
    pygame.Rect(700, 100, 20, 20)
]
itens_coletados = 0
ganhou = False

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and byte_x > 0:
        byte_x -= velocidade
    if teclas[pygame.K_RIGHT] and byte_x < LARGURA - byte_width:
        byte_x += velocidade
    if teclas[pygame.K_UP] and byte_y > 0:
        byte_y -= velocidade
    if teclas[pygame.K_DOWN] and byte_y < ALTURA - byte_height:
        byte_y += velocidade

    byte_rect = pygame.Rect(byte_x, byte_y, byte_width, byte_height)
    
    colidiu = False
    for obstaculo in obstaculos:
        if byte_rect.colliderect(obstaculo) and not colidiu:
            colisoes += 1
            byte_x = 50
            byte_y = ALTURA - byte_height - 10
            colidiu = True

    for item in itens[:]:
        if byte_rect.colliderect(item):
            itens.remove(item)
            itens_coletados += 1

    if colisoes >= 3:
        print("Game Over! Você colidiu 3 vezes.")
        executando = False

    if itens_coletados >= 3 and not ganhou:
        print("Você ganhou!")
        ganhou = True
        executando = False

    tela.fill(BRANCO)
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, PRETO, obstaculo)
    for item in itens:
        pygame.draw.rect(tela, VERMELHO, item)
    tela.blit(byte_img, (byte_x, byte_y))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
