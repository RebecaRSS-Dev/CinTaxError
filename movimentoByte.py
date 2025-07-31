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
byte_jump_speed_inicial = -15
byte_jump_speed = byte_jump_speed_inicial
byte_gravity = 1

obstaculo_width = 30
obstaculo_height = 70
obstaculo_x = LARGURA 
obstaculo_y_inicial = ALTURA - obstaculo_height - 10
obstaculo_y = obstaculo_y_inicial
velocidade_do_obstaculo = 5

clock = pygame.time.Clock() 

executando = True

while(executando): 
    for evento in pygame.event.get(): 
        if  evento.type == pygame.QUIT: 
            running = False
        elif evento.type == pygame.KEYDOWN: 
            # if  evento.key == pygame.K_SPACE and byte_y == byte_y_inicial: 
            #     byte_jump_speed = byte_jump_speed_inicial
            if evento.key == pygame.K_UP:
                byte_jump_speed = byte_y_inicial - 50
        byte_jump_speed += byte_gravity
        
    byte_y += byte_jump_speed 

    if byte_y > byte_y_inicial: 
        byte_y = byte_y_inicial
        byte_jump_speed = 0
        
    # obstaculo_x -= velocidade_do_obstaculo
    
    # if obstaculo_x < -obstaculo_width: 
    #     obstaculo_x = LARGURA 
    #     obstaculo_y = obstaculo_y_inicial 

    if ( 
        byte_x + byte_width > obstaculo_x 
        and byte_x < obstaculo_x + obstaculo_width 
        and byte_y + byte_height > obstaculo_y 
    ):
        executando = False 

    tela.fill(BRANCO) 

    pygame.draw.rect(tela, PRETO, (byte_x, byte_y, byte_width, byte_height))
    pygame.draw.rect(tela, PRETO, (obstaculo_x, obstaculo_y, obstaculo_width, obstaculo_height)) 

    pygame.display.flip() 

    clock.tick( 60 )

pygame.quit() 
