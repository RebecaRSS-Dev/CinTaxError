import pygame

pygame.init()

# --- Configurações e Cores ---
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Coletáveis com Efeitos Diferentes")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
CIANO = (0, 255, 255)


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
        
    #desenhar:
    def desenhar (self, tela):
        pygame.draw.rect (tela, self.cor, self.rect)
        

# --- Variáveis do Jogo ---
player_rect = pygame.Rect(350, 250, 50, 50)
VELOCIDADE_NORMAL = 7
velocidade_jogador = VELOCIDADE_NORMAL
pontuacao = 0
fonte = pygame.font.Font(None, 50)
cor_jogador = VERMELHO

# ### NOVAS VARIÁVEIS PARA CONTROLE DE EFEITOS ###
escudo_ativo = False
# Timers: guardam o momento em que o efeito deve acabar
# pygame.time.get_ticks() retorna o tempo em milissegundos desde que o jogo começou
tempo_fim_velocidade = 0
tempo_fim_escudo = 0
DURACAO_EFEITO_MS = 5000 # 5000 milissegundos = 5 segundos

# --- Criando os Coletáveis de cada tipo ---
lista_de_coletaveis = [
    Coletavel(100, 100, tipo=1), # Coletável de pontos
    Coletavel(600, 400, tipo=2), # Coletável de velocidade
    Coletavel(300, 500, tipo=3)  # Coletável de escudo
]

rodando = True

while (rodando):
    #pegar o momento de agora 
    agora = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if (evento.type == pygame.QUIT):
            rodando = False
    
    
    # --- LÓGICA DOS TIMERS (verificar se os efeitos acabaram) ---
    if velocidade_jogador > VELOCIDADE_NORMAL and agora > tempo_fim_velocidade:
        print("Efeito de velocidade acabou.")
        velocidade_jogador = VELOCIDADE_NORMAL
    
    if escudo_ativo and agora > tempo_fim_escudo:
        print("Efeito de escudo acabou.")
        escudo_ativo = False
        cor_jogador = VERMELHO
    
     # --- Movimento do Jogador ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= velocidade_jogador
    if teclas[pygame.K_RIGHT] and player_rect.right < LARGURA_TELA: player_rect.x += velocidade_jogador
    if teclas[pygame.K_UP] and player_rect.top > 0: player_rect.y -= velocidade_jogador
    if teclas[pygame.K_DOWN] and player_rect.bottom < ALTURA_TELA: player_rect.y += velocidade_jogador

    #impedir dele sair da tela:


    for item in lista_de_coletaveis[:]:
        if (player_rect.colliderect(item.rect)):
            if (item.tipo == 1):
                pontuacao += item.pontos
            
            elif (item.tipo == 2):
                velocidade_jogador = VELOCIDADE_NORMAL + 5
                tempo_fim_velocidade = agora + DURACAO_EFEITO_MS
            
            elif (item.tipo == 3):
                escudo_ativo = True
                tempo_fim_escudo = agora + DURACAO_EFEITO_MS

            lista_de_coletaveis.remove(item)
    
    #desenhar o jogador
    tela.fill(PRETO)
    if (escudo_ativo):
        cor_jogador = CIANO
    
    pygame.draw.rect(tela, cor_jogador, player_rect)

    for item in lista_de_coletaveis:
        item.desenhar(tela)
    
    # Desenha a pontuação na tela
    texto_pontuacao = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (10, 10))



    # --- Atualização da Tela ---
    pygame.display.flip()
    pygame.time.Clock().tick(60)


pygame.quit()