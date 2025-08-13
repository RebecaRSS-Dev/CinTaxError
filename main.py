import pygame
from Services.Niveis import Niveis
from Services.Player import Player
from graphics.Cores import Cores
from Services.Botao import Botao
from Services.Obstaculo import Obstacle
pygame.init()

#Configuração Geral
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

largura_tela, altura_tela = screen.get_size()

#Fontes:
fonte_pequena = pygame.font.Font('./ari-w9500-bold.ttf', 20)
fonte_grande = pygame.font.Font('./ari-w9500-bold.ttf', 36)
        
class Fluxo:
    # --- Seção de carregamento e posicionamento ---
    def __init__(self):
        self.derrotado = False
        self.vitoria = False
        self.start = True
        self.jogando = False
        self.rodando = True

        try:
            # Telas
            self.imagem_tela_start = pygame.transform.scale(pygame.image.load('imagens/Telas/Tela inicial.jpg').convert(), (largura_tela, altura_tela))
            self.imagem_tela_gameover = pygame.transform.scale(pygame.image.load('imagens/Telas/Game Over.jpg').convert(), (largura_tela, altura_tela))
            self.imagem_tela_vitoria = pygame.transform.scale(pygame.image.load('imagens/Telas/You Win.jpg').convert(), (largura_tela, altura_tela))

            # Botões start
            self.botao_jogar_img = pygame.image.load('imagens/Telas/Botao_start.png').convert_alpha()
            self.botao_jogar_selecionado_img = pygame.image.load('imagens/Telas/Botao_start_selecionado.png').convert_alpha()

            # Botões restart
            self.botao_restart_img = pygame.image.load('imagens/Telas/Restart.png').convert_alpha()
            self.botao_restart_selecionado_img = pygame.image.load('imagens/Telas/Restart Hover.png').convert_alpha()

            # Botões sair
            self.botao_sair_img = pygame.image.load('imagens/Telas/Botao_quit.png').convert_alpha()
            self.botao_sair_selecionado_img = pygame.image.load('imagens/Telas/Botao_quit_selecionado.png').convert_alpha()

        except pygame.error as e:
            print(f"Erro ao carregar imagens: {e}")

        # --- Botões tela inicial ---
        pos_y_jogar = altura_tela * 0.80 - ((self.botao_jogar_img.get_height() + 20 + self.botao_sair_img.get_height()) / 2) + (self.botao_jogar_img.get_height() / 2)
        pos_y_sair = altura_tela * 0.80 + (self.botao_jogar_img.get_height() + 20 + self.botao_sair_img.get_height() / 2) - (self.botao_sair_img.get_height() / 2)
        pos_x_botoes = largura_tela // 2

        self.botao_jogar = Botao(pos_x_botoes, int(pos_y_jogar), self.botao_jogar_img, self.botao_jogar_selecionado_img)
        self.botao_sair = Botao(pos_x_botoes, int(pos_y_sair), self.botao_sair_img, self.botao_sair_selecionado_img)
        self.lista_de_botoes = [self.botao_jogar, self.botao_sair]

        # --- Botões tela de Game Over ---
        pos_y_botoes = altura_tela * 0.90
        pos_x_restart = largura_tela * 0.20
        pos_x_sair_go = largura_tela * 0.80
        self.botao_restart = Botao(int(pos_x_restart), pos_y_botoes, self.botao_restart_img, self.botao_restart_selecionado_img)
        self.botao_sair_go = Botao(int(pos_x_sair_go), pos_y_botoes, self.botao_sair_img, self.botao_sair_selecionado_img)
        self.botoes_gameover = [self.botao_restart, self.botao_sair_go]

    def telaDeStart(self, tela, botao_sair, botao_jogar, lista_de_botoes, imagem_tela_start):
        posicao_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.rect.collidepoint(posicao_mouse):
                    self.rodando = False
                    pygame.quit()
                    exit()
                if botao_jogar.rect.collidepoint(posicao_mouse):
                    self.jogando = True
                    self.start = False

        tela.blit(imagem_tela_start, (0, 0))
        for botao in lista_de_botoes:
            botao.checar_hover(posicao_mouse)
            botao.desenhar(tela)

    def telaDeGameOver(self):
        posicao_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_sair_go.rect.collidepoint(posicao_mouse):
                    self.rodando = False
                    pygame.quit()
                    exit()
                if self.botao_restart.rect.collidepoint(posicao_mouse):
                    global nivelAtual, ObjNivel, ObjetosNiveis
                    ObjetosNiveis = criar_niveis()
                    nivelAtual = 'Hub'
                    ObjNivel = ObjetosNiveis[nivelAtual]
                    
                    # Reseta posição e atributos importantes do player
                    ObjNivel.player.rect.center = ObjNivel.player_pos
                    ObjNivel.player.vidas = 3  # ou o valor padrão que quiser
                    ObjNivel.player.pontuacao = 0
                    ObjNivel.player.fragmentos = 0
                    ObjNivel.player.velocidade = 4  # velocidade padrão
                    ObjNivel.player.efeito = None  # se for usado

                    self.jogando = True
                    self.derrotado = False

        screen.blit(self.imagem_tela_gameover, (0, 0))
        for botao in self.botoes_gameover:
            botao.checar_hover(posicao_mouse)
            botao.desenhar(screen)

    def telaDeVitoria(self):
        posicao_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_sair_go.rect.collidepoint(posicao_mouse):
                    self.rodando = False
                    pygame.quit()
                    exit()
                if self.botao_restart.rect.collidepoint(posicao_mouse):
                    global nivelAtual, ObjNivel, ObjetosNiveis
                    ObjetosNiveis = criar_niveis()
                    nivelAtual = 'Hub'
                    ObjNivel = ObjetosNiveis[nivelAtual]
                    
                     # Reseta posição e atributos importantes do player
                    ObjNivel.player.rect.center = ObjNivel.player_pos
                    ObjNivel.player.vidas = 3
                    ObjNivel.player.pontuacao = 0
                    ObjNivel.player.fragmentos = 0
                    ObjNivel.player.velocidade = 4
                    ObjNivel.player.efeito = None

                    # Reseta os estados do fluxo de jogo
                    self.jogando = True
                    self.vitoria = False

        # Desenha a tela de fundo e os botões
        screen.blit(self.imagem_tela_vitoria, (0, 0))
        for botao in self.botoes_gameover: # Reutilizando os botões da tela de Game Over
            botao.checar_hover(posicao_mouse)
            botao.desenhar(screen)        
            

    def jogo(self, player, NivelAtual, grupo_colisao, Inimigos, Coletaveis, grupo_inimigos):
        teclasPressionadas = pygame.key.get_pressed()
        player.mover(teclasPressionadas, grupo_colisao, Inimigos)
        screen.fill(Cores.PRETO)
        NivelAtual.desenhar_mapa(screen)
        player.desenhar(screen)
        player.efeitos(Coletaveis)

        for coletavel in Coletaveis:
            coletavel.update(player.fragmentos)
            coletavel.desenhar(screen)
            #pygame.draw.rect(screen, coletavel.cor, coletavel.rect, 2)

        for inimigo in Inimigos:
            inimigo.move(player, grupo_colisao, Inimigos)
            inimigo.update()
            inimigo.draw(screen)


# Dicionário que define quantos fragmentos são necessários para cada sala
REQUISITOS_FRAGMENTOS = {
    1: 0,  # Sala 1 não precisa de fragmentos para entrar
    2: 1,  # Sala 2 precisa de 1 fragmento
    3: 2,  # Sala 3 precisa de 2 fragmentos
    4: 3   # Sala 4 precisa de 3 fragmentos
}

player = Player(0,0,40,40)

def criar_niveis():
    return {
        'Hub': Niveis('mapas prontos/entrada.tmx',player, largura_tela, altura_tela),
        1: Niveis('mapas prontos/sala1.tmx',player, largura_tela, altura_tela), 
        2: Niveis('mapas prontos/sala2.tmx',player, largura_tela, altura_tela),
        3: Niveis('mapas prontos/sala3.tmx',player, largura_tela, altura_tela),
        4: Niveis('mapas prontos/sala4.tmx',player, largura_tela, altura_tela),
    }

fluxoDeJogo = Fluxo()
ObjetosNiveis = criar_niveis()
nivelAtual = 'Hub'



teleporte_cooldown = 0  # global

def irParaHub():
    global ObjNivel, nivelAtual, teleporte_cooldown
    if ObjNivel.player.mudarFase:
        nivelAtual = 'Hub'
        ObjNivel.player.mudarFase = False
        ObjNivel = ObjetosNiveis[nivelAtual]
        ObjNivel.player.rect.center = ObjNivel.player_pos
        teleporte_cooldown = 300  # meio segundo de cooldown a 60fps

        return ObjNivel.player.vidas, ObjNivel.player.pontuacao, ObjNivel.player.efeito, ObjNivel.player.fragmentos
    return None, None, None, None



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

        vida, pontuacao, efeito, fragmentos = irParaHub()
        
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
            texto_efeito = fonte_grande.render(f"Efeito: {ObjNivel.player.efeito}", False, Cores.BRANCO)
            screen.blit(texto_efeito, (largura_tela*0.82, 80))

    pygame.display.flip()
    pygame.time.Clock().tick(60)