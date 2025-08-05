import pygame 

screen = [1, 1, 2, 2, 2, 1]
print(screen)
[1, 1, 2, 2, 2, 1]

screen[3] = 8
print(screen)
[1, 1, 2, 8, 2, 1]

playerpos = 3
screen[playerpos] = 8
print(screen)
[1, 1, 2, 8, 2, 1]

background = [1, 1, 2, 2, 2, 1]
screen = [0]*6             
for i in range(6):
    screen[i] = background[i]
print(screen)
[1, 1, 2, 2, 2, 1]
playerpos = 3
screen[playerpos] = 8
print(screen)
[1, 1, 2, 8, 2, 1]


print(screen)
[1, 1, 2, 8, 2, 1]
screen[playerpos] = background[playerpos]
playerpos = playerpos - 1
screen[playerpos] = 8
print(screen)
[1, 1, 8, 2, 2, 1]

screen[playerpos] = background[playerpos]
playerpos = playerpos - 1
screen[playerpos] = 8
print(screen)
[1, 8, 2, 2, 2, 1]

pygame.image.load("caminho/para/imagem.png")

background = [terrain1, terrain1, terrain2, terrain2, terrain2, terrain1]
screen = create_graphics_screen()
for i in range(6):
    screen.blit(background[i], (i*10, 0))
playerpos = 3
screen.blit(playerimage, (playerpos*10, 0))



import pygame

pygame.init()

LARGURA = 800
ALTURA = 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Byte Game")

BRANCO = (255, 255, 255)
byte_height = 800  * 0.20
byte_width = byte_height * 0.40

byte_img = pygame.image.load("./front_byte1.1.png")
byte_img = pygame.transform.scale(byte_img, (byte_width // 2, byte_height // 2))
byte_width, byte_height = byte_img.get_size()

byte_jump_speed_inicial = -15
byte_jump_speed = byte_jump_speed_inicial
byte_gravity = 1

byte_x = 50
byte_y_inicial = ALTURA - byte_height - 10
byte_y = byte_y_inicial

velocidade = 5

clock = pygame.time.Clock()

executando = True
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
#     if  teclas[pygame.K_SPACE] and byte_y == byte_y_inicial: 
#         byte_jump_speed = byte_jump_speed_inicial
        
#     byte_jump_speed += byte_gravity
    
# byte_y += byte_jump_speed 

tela.fill(BRANCO)
tela.blit(byte_img, (byte_x, byte_y))
pygame.display.flip()

clock.tick(60)

pygame.quit()