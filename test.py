import pygame # type: ignore

pygame.init()

# --- Configurações da Janela ---
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Hub Central e Fases")

# --- Cores e Fonte ---
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0) # ### NOVO: Para portas abertas
CINZA = (100, 100, 100) # ### NOVO: Para portas fechadas
fonte = pygame.font.Font(None, 50)
fonte_pequena = pygame.font.Font(None, 30) # ### NOVO: Para os números das portas

# --- CARREGANDO ASSETS ---
try:
    # ### NOVO: Carregando a imagem do Hub
    fundo_hub = pygame.image.load('fundo_hub.jpg').convert()
    fundo_fase1 = pygame.image.load('mapa1.jpg').convert()
    fundo_fase2 = pygame.image.load('mapa2.jpg').convert()
    fundo_fase3 = pygame.image.load('mapa3.jpg').convert()
    # Adicione uma quarta imagem de fase se desejar
    # fundo_fase4 = pygame.image.load('fundo_fase4.jpg').convert() 
except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    pygame.quit()
    exit()

# Redimensionando imagens
fundo_hub = pygame.transform.scale(fundo_hub, (LARGURA_TELA, ALTURA_TELA))
fundo_fase1 = pygame.transform.scale(fundo_fase1, (LARGURA_TELA, ALTURA_TELA))
fundo_fase2 = pygame.transform.scale(fundo_fase2, (LARGURA_TELA, ALTURA_TELA))
fundo_fase3 = pygame.transform.scale(fundo_fase3, (LARGURA_TELA, ALTURA_TELA))

# --- ESTRUTURA DE DADOS DOS NÍVEIS ---
niveis = {
    1: {"fundo": fundo_fase1, "coletaveis": [pygame.Rect(100, 450, 30, 30), pygame.Rect(700, 500, 30, 30)]},
    2: {"fundo": fundo_fase2, "coletaveis": [pygame.Rect(50, 100, 30, 30), pygame.Rect(700, 400, 30, 30)]},
    3: {"fundo": fundo_fase3, "coletaveis": [pygame.Rect(150, 500, 30, 30), pygame.Rect(650, 80, 30, 30)]},
    # Adicione a fase 4 aqui quando tiver
    # 4: {"fundo": fundo_fase4, "coletaveis": [ ... ]}
}

# --- ### NOVO: DEFINIÇÃO DAS PORTAS NO HUB ---
# Um dicionário onde a chave é o número da fase que a porta leva
portas = {
    1: pygame.Rect(100, 50, 80, 120),  # Porta da Fase 1 (x, y, largura, altura)
    2: pygame.Rect(300, 50, 80, 120),  # Porta da Fase 2
    3: pygame.Rect(500, 50, 80, 120),  # Porta da Fase 3
    4: pygame.Rect(700, 50, 80, 120)   # Porta da Fase 4
}


# --- Variáveis do Jogo ---
player_rect = pygame.Rect(350, 450, 50, 50) # Posição inicial no hub
velocidade_jogador = 5
pontuacao_total = 0

# --- ### NOVO: Variáveis de Controle de Estado e Progresso ---
estado_jogo = "hub"  # Começamos no hub
nivel_maximo_liberado = 1 # O jogador começa com a fase 1 liberada
fase_atual = 0 # Nenhuma fase está ativa no início
coletaveis_ativos = []
jogo_finalizado = False

# --- Loop Principal do Jogo ---
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # --- MOVIMENTO (Comum para Hub e Fase) ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= velocidade_jogador
    if teclas[pygame.K_RIGHT] and player_rect.right < LARGURA_TELA: player_rect.x += velocidade_jogador
    if teclas[pygame.K_UP] and player_rect.top > 0: player_rect.y -= velocidade_jogador
    if teclas[pygame.K_DOWN] and player_rect.bottom < ALTURA_TELA: player_rect.y += velocidade_jogador

    # --- LÓGICA DO JOGO BASEADA NO ESTADO ---
    
    if estado_jogo == "hub":
        # --- LÓGICA DO HUB ---
        tela.blit(fundo_hub, (0, 0)) # Desenha o fundo do hub

        # Desenhar as portas e checar colisão
        for num_fase, porta_rect in portas.items():
            if num_fase <= nivel_maximo_liberado:
                cor_porta = VERDE # Porta liberada
            else:
                cor_porta = CINZA # Porta bloqueada
            
            pygame.draw.rect(tela, cor_porta, porta_rect)
            
            # Desenha o número da fase na porta
            texto_porta = fonte_pequena.render(str(num_fase), True, BRANCO)
            pos_texto = texto_porta.get_rect(center=porta_rect.center)
            tela.blit(texto_porta, pos_texto)

            # Checar se o jogador entra em uma porta LIBERADA
            if player_rect.colliderect(porta_rect) and num_fase <= nivel_maximo_liberado:
                if num_fase in niveis: # Verifica se a fase existe no nosso dicionário
                    print(f"Entrando na fase {num_fase}...")
                    estado_jogo = "em_fase"
                    fase_atual = num_fase
                    coletaveis_ativos = niveis[fase_atual]["coletaveis"].copy()
                    player_rect.center = (LARGURA_TELA / 2, ALTURA_TELA - 100) # Posição inicial dentro da fase
                    break # Sai do loop for para evitar entrar em múltiplas portas

    elif estado_jogo == "em_fase":
        # --- LÓGICA DA FASE (código que já tínhamos) ---
        tela.blit(niveis[fase_atual]["fundo"], (0, 0)) # Desenha o fundo da fase

        # Coletar itens
        for coletavel in coletaveis_ativos[:]: 
            if player_rect.colliderect(coletavel):
                pontuacao_total += 1
                coletaveis_ativos.remove(coletavel)
        
        # Desenhar coletáveis restantes
        for coletavel in coletaveis_ativos:
            pygame.draw.rect(tela, AZUL, coletavel)

        # Checar se a fase foi concluída
        if not coletaveis_ativos:
            print(f"Fase {fase_atual} concluída!")
            # ### NOVO: Lógica de retorno ao Hub
            nivel_maximo_liberado = max(nivel_maximo_liberado, fase_atual + 1)
            estado_jogo = "hub"
            player_rect.center = (LARGURA_TELA / 2, ALTURA_TELA / 2) # Reposiciona no meio do hub

            # Checar condição de vitória final
            if nivel_maximo_liberado > len(niveis):
                 jogo_finalizado = True


    # --- DESENHO COMUM ---
    if jogo_finalizado:
        texto_vitoria = fonte.render("VOCÊ COMPLETOU O JOGO!", True, VERDE)
        pos_texto = texto_vitoria.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))
        tela.blit(texto_vitoria, pos_texto)
    else:
        # Desenha o jogador
        pygame.draw.rect(tela, VERMELHO, player_rect)
        # Desenha a pontuação total
        texto_pontuacao = fonte.render(f"Pontos: {pontuacao_total}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, ALTURA_TELA - 40))

    # --- Atualização da Tela ---
    pygame.display.flip()
    pygame.time.Clock().tick(60)


pygame.quit()