import pygame
from graphics.Cores import Cores
from ui.Botao import Botao
from ui.ConfigsTela import ConfigsTela

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
            self.imagem_tela_win = pygame.transform.scale(pygame.image.load('imagens\Telas\You Win.jpg').convert(), (largura_tela, altura_tela))

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
                    ObjetosNiveis = configs.niveis  # Acessa o dicionário de níveis da configuração global
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
                    ObjetosNiveis = configs.niveis  # Acessa o dicionário de níveis da configuração global
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
                    self.vitoria = False

        # Desenha a tela de fundo e os botões
        screen.blit(self.imagem_tela_win, (0, 0))
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

configs = ConfigsTela()

# Acessar os atributos
largura_tela = configs.largura_tela
altura_tela = configs.altura_tela
screen = configs.screen
player = configs.player_posicao
