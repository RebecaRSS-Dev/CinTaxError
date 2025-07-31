import pygame 

pygame.init() 

LARGURA = 800
ALTURA = 400
tela = pygame.display.set_mode((LARGURA, ALTURA)) 
pygame.display.set_caption( "Byte Game" ) 

BRANCO = ( 255 , 255 , 255 ) 
PRETO = ( 0 , 0 , 0 ) 

byte_width = 40
byte_height = 60
byte_x = 50
byte_y_inicial = ALTURA - byte_height - 10
byte_y = byte_y_inicial
byte_jump_speed = - 15
byte_gravity = 0.8

largura_do_obstaculo = 30
altura_do_obstaculo = 70
obstaculo_x = LARGURA 
obstaculo_y_inicial = ALTURA - altura_do_obstaculo - 10
obstaculo_y = obstaculo_y_inicial
velocidade_do_obstaculo = 5

relógio = pygame.time.Clock() 

executando = True

while(executando): 
    for evento in pygame.event.get(): 
        if  evento.type == pygame.QUIT: 
            running = False
        elif evento.type == pygame.KEYDOWN: 
            if  evento.key == pygame.K_SPACE and byte_y == byte_y_inicial : byte_jump_speed             = - 15