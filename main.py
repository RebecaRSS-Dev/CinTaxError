import pygame
from niveis.Transicoes import Transicoes
from entidades.Player import Player
from graphics.Cores import Cores
from entidades.Obstaculo import Obstacle
from ui.Fluxo import Fluxo
from ui.ConfigsTela import ConfigsTela

pygame.init()
# Instanciar a classe ConfigsTela
configs = ConfigsTela()

# Acessar os atributos
screen = configs.screen
largura_tela = configs.largura_tela
altura_tela = configs.altura_tela
fonte_pequena = configs.fonte_pequena
fonte_grande = configs.fonte_grande
        
# Dicionário que define quantos fragmentos são necessários para cada sala
REQUISITOS_FRAGMENTOS = configs.REQUISITOS_FRAGMENTOS
# Inicializações
player = configs.player_posicao
fluxoDeJogo = Fluxo()
ObjetosNiveis = configs.niveis
nivelAtual = 'Hub'
teleporte_cooldown = 0
transicoes = Transicoes()

def atualizar_portais_obstaculos(player, portais, grupo_obstaculos):
    """
    Limpa o grupo de obstáculos de portais e o preenche novamente com
    os portais que estão atualmente bloqueados.
    """
    grupo_obstaculos.empty()
    for nome_sala, portal_rect in portais.items():
        try:
            num_sala = int(nome_sala.replace('sala', ''))
            fragmentos_necessarios = REQUISITOS_FRAGMENTOS.get(num_sala, 999)
            if player.fragmentos < fragmentos_necessarios:
                obstaculo_portal = Obstacle(portal_rect)
                grupo_obstaculos.add(obstaculo_portal)
        except (ValueError, KeyError):
            continue


def checar_portais_e_mudar_nivel():
    """Verifica se o jogador colide com um portal e tem fragmentos suficientes."""
    global nivelAtual, ObjNivel

    # A verificação só acontece se o jogador estiver no Hub
    if nivelAtual == 'Hub':
        player = ObjNivel.player
        # Itera sobre os portais definidos no nível Hub
        for nome_sala, portal_rect in ObjNivel.portais.items():
            # 1. Checa a colisão entre o jogador e o retângulo do portal
            if player.rect.colliderect(portal_rect):
                try:
                    # Extrai o número da sala do nome do objeto (ex: 'sala1' -> 1)
                    num_sala = int(nome_sala.replace('sala', ''))
                    
                    # 2. Checa se o jogador tem os fragmentos necessários
                    fragmentos_necessarios = REQUISITOS_FRAGMENTOS.get(num_sala, 999)
                    if player.fragmentos == fragmentos_necessarios:
                        nivelAtual = num_sala # Muda o nível atual para o número da sala
                        ObjNivel = ObjetosNiveis[nivelAtual]
                        ObjNivel.player.rect.center = ObjNivel.player_pos
                        break # Para o loop assim que um portal é ativado
                except (ValueError, KeyError):
                    continue

# Loop principal do jogo
while True:
    
    if fluxoDeJogo.start:
        fluxoDeJogo.telaDeStart(screen, fluxoDeJogo.lista_de_botoes[1], fluxoDeJogo.lista_de_botoes[0], fluxoDeJogo.lista_de_botoes, fluxoDeJogo.imagem_tela_start)
    
    if fluxoDeJogo.jogando:
        
        ObjNivel = ObjetosNiveis[nivelAtual]
        
        # Atualiza quais portais são obstáculos neste quadro
        if nivelAtual == 'Hub':
            atualizar_portais_obstaculos(ObjNivel.player, ObjNivel.portais, ObjNivel.grupo_portais_obstaculos)

        # Cria um grupo de colisão total para este quadro
        grupo_colisao_total = pygame.sprite.Group()
        grupo_colisao_total.add(ObjNivel.grupo_colisao)
        grupo_colisao_total.add(ObjNivel.grupo_portais_obstaculos)

        Inimigos = ObjNivel.grupo_inimigos
        Coletaveis = ObjNivel.grupo_colecionaveis
        grupo_inimigos = pygame.sprite.Group(Inimigos)
        
        
        ObjNivel, nivelAtual, vida, pontuacao, efeito, fragmentos, teleporte_cooldown = transicoes.irParaHub(ObjNivel, ObjetosNiveis, nivelAtual, teleporte_cooldown)
        
        if vida is not None:
            ObjNivel.player.vidas = vida
            ObjNivel.player.pontuacao = pontuacao
            ObjNivel.player.efeito = efeito
            ObjNivel.player.fragmentos = fragmentos
        
        # Passa o grupo de colisão TOTAL para a função de jogo
        fluxoDeJogo.jogo(ObjNivel.player, ObjNivel, grupo_colisao_total, Inimigos, Coletaveis, grupo_inimigos)

        if teleporte_cooldown > 0:
            teleporte_cooldown -= 1
        else:
            checar_portais_e_mudar_nivel()
        
        # Código para desenhar os portais liberados (se desejar)
        if nivelAtual == 'Hub':
            COR_LIBERADO = (0, 0, 0)
            player = ObjNivel.player
            for nome_sala, portal_rect in ObjNivel.portais.items():
                try:
                    num_sala = int(nome_sala.replace('sala', ''))
                    fragmentos_necessarios = REQUISITOS_FRAGMENTOS.get(num_sala, 999)
                    if player.fragmentos == fragmentos_necessarios:
                        forma_portal = pygame.Surface(portal_rect.size, pygame.SRCALPHA)
                        pygame.draw.rect(forma_portal, COR_LIBERADO, forma_portal.get_rect())
                        screen.blit(forma_portal, portal_rect.topleft)
                except (ValueError, KeyError):
                    continue
        
        if ObjNivel.player.vidas <= 0:
            fluxoDeJogo.jogando = False
            fluxoDeJogo.derrotado = True
        
        if ObjNivel.player.fragmentos >= 4 and nivelAtual == 'Hub':
            fluxoDeJogo.jogando = False
            fluxoDeJogo.vitoria = True
    
    #ver se o jogo terminou ou se o jogador venceu
    if fluxoDeJogo.derrotado:
        fluxoDeJogo.telaDeGameOver()
    
    if fluxoDeJogo.vitoria:
        fluxoDeJogo.telaDeVitoria()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Desenha a pontuação na tela

    if fluxoDeJogo.start == False and fluxoDeJogo.jogando == True:
        texto_pontuacao = fonte_grande.render(f"Pontos: {ObjNivel.player.pontuacao}", False, Cores.BRANCO)
        screen.blit(texto_pontuacao, (10, 10))
        texto_fragmentos = fonte_grande.render(f"Fragmentos: {ObjNivel.player.fragmentos}", False, Cores.BRANCO)
        screen.blit(texto_fragmentos, (10, 80))
        texto_vidas = fonte_grande.render(f"Vidas: {ObjNivel.player.vidas}", False, Cores.BRANCO)
        screen.blit(texto_vidas, (largura_tela*0.90, 10))
        
        if not (ObjNivel.player.efeito):
            texto_efeito = fonte_grande.render("Efeito: Nenhum", False, Cores.BRANCO)
            screen.blit(texto_efeito, (largura_tela*0.85, 80))
        else:
            if (ObjNivel.player.efeito == 'velocidade'):
                texto_efeito = fonte_grande.render(f"Efeito: {ObjNivel.player.efeito}", False, Cores.BRANCO)
                screen.blit(texto_efeito, (largura_tela*0.82, 80))
            else:
                fonte_grande_1 = pygame.font.Font('./graphics/fonts/ari-w9500-bold.ttf', 28)
                texto_efeito = fonte_grande_1.render(f"Efeito: {ObjNivel.player.efeito}", False, Cores.BRANCO)
                screen.blit(texto_efeito, (largura_tela*0.82, 80))

    pygame.display.flip()
    pygame.time.Clock().tick(60)