import pygame
import random

pygame.init()

#configuração da tela:
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption ("Teste dos coletáveis")

#---Carregar is assents-----
#carregar as imagens
try:
    fundo_fase1 = pygame.image.load('mapa1.jpg').convert()
    fundo_fase2 = pygame.image.load('mapa2.jpg').convert()
    fundo_fase3 = pygame.image.load('mapa3.jpg').convert()
except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    print("Certifique-se que os arquivos 'fundo_fase1.jpg', 'fundo_fase2.jpg' e 'fundo_fase3.jpg' estão na pasta do projeto.")
    pygame.quit()
    exit()

#arrumar os tamanhos:
fundo_fase1 = pygame.transform.scale(fundo_fase1, (largura_tela, altura_tela))
fundo_fase2 = pygame.transform.scale(fundo_fase2, (largura_tela, altura_tela))
fundo_fase3 = pygame.transform.scale(fundo_fase3, (largura_tela, altura_tela))

#variáveis do jogo:
player_rect = pygame.Rect(350, 250, 50, 50)
velocidade_jogador = 5

#coletaveis:
niveis = {
    1: {
        "fundo": fundo_fase1,
        "coletaveis": [
            pygame.Rect(100, 450, 30, 30),
            pygame.Rect(400, 200, 30, 30),
            pygame.Rect(700, 500, 30, 30)
        ]
    },
    2: {
        "fundo": fundo_fase2,
        "coletaveis": [
            pygame.Rect(50, 100, 30, 30),
            pygame.Rect(250, 300, 30, 30),
            pygame.Rect(550, 150, 30, 30),
            pygame.Rect(700, 400, 30, 30) # A fase 2 pode ter mais coletáveis!
        ]
    },
    3: {
        "fundo": fundo_fase3,
        "coletaveis": [
            pygame.Rect(150, 500, 30, 30),
            pygame.Rect(650, 80, 30, 30)
        ]
    }
}

#organização das fases:
fase_atual = 1
coletaveis_ativos = niveis[fase_atual]["coletaveis"].copy() 
jogo_finalizado = False

#variavel de contador de coletaveis:
pontuacao = 0
fonte = pygame.font.Font(None, 50)


#----Loop Princial do jogo-----
rodando = True

while (rodando):

    #analise dos eventos:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    if (not jogo_finalizado):

        # --- Movimento do Jogador ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and player_rect.right < largura_tela:
            player_rect.x += velocidade_jogador
        if teclas[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= velocidade_jogador
        if teclas[pygame.K_DOWN] and player_rect.bottom < altura_tela:
            player_rect.y += velocidade_jogador

        
        #logica dos coletaveis:
        coletaveis_coletados = []
        for coletavel in coletaveis_ativos[:]:
            if (player_rect.colliderect(coletavel)):
                pontuacao += 1
                coletaveis_ativos.remove(coletavel)
        
        if (not coletaveis_ativos):
            fase_atual += 1

            if fase_atual in niveis:
                print (f"Parabéns! Indo para a fase {fase_atual}")
                coletaveis_ativos = niveis[fase_atual]["coletaveis"].copy()

                player_rect.center = (largura_tela / 2, altura_tela / 2)
            
            else:
                print ("Você venceu")
                jogo_finalizado = True
        
        # ---- Desenhar na tela -----

        fundo_atual = niveis.get(fase_atual, {}).get("fundo", fundo_fase3)
        tela.blit (fundo_atual, (0,0))

        if not (jogo_finalizado):

            #desenhar o jogador:
            pygame.draw.rect(tela, (255,0,0), player_rect)

            #desenhar os coletaveis:
            for coletavel in coletaveis_ativos:
                pygame.draw.rect(tela,(0,255,0), coletavel)

            #desenhar a pontuação:
            texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, (255, 255, 255))
            tela.blit (texto_pontuacao, (10,10))

            # Desenha a pontuação
            texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, (255,255,255))
            tela.blit(texto_pontuacao, (10, 10))

        else:
            #mostrar vitoria
            texto_vitoria = fonte.render("VOCÊ VENCEU!", True, (255, 255, 255))
            pos_texto = texto_vitoria.get_rect(center = (largura_tela / 2, altura_tela / 2))
            tela.blit(texto_vitoria, pos_texto)
    
    #configurações especificas:
        pygame.display.flip()
        pygame.time.Clock().tick(60)

pygame.quit()