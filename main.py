import pygame
from Services.Niveis import Niveis
from graphics.Cores import Cores
from Services.Botao import Botao
pygame.init()

#Configuração Geral
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

largura_tela, altura_tela = screen.get_size()

#Fontes:
fonte_pequena = pygame.font.Font('ari-w9500-bold.ttf', 20)
fonte_grande = pygame.font.Font('ari-w9500-bold.ttf', 36)
        
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
                    nivelAtual = 1
                    ObjNivel = ObjetosNiveis[nivelAtual]
                    self.jogando = True
                    self.derrotado = False


        screen.blit(self.imagem_tela_gameover, (0, 0))
        for botao in self.botoes_gameover:
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
            coletavel.update()
            coletavel.desenhar(screen)
            pygame.draw.rect(screen, coletavel.cor, coletavel.rect, 2)

        for inimigo in Inimigos:
            inimigo.move(player, grupo_colisao, Inimigos)
            inimigo.update()
            inimigo.draw(screen)

        pygame.draw.rect(screen, (255, 255, 0), player.rect, 2)
        grupo_colisao.draw(screen)
        for inim in grupo_inimigos:
            pygame.draw.rect(screen, (0, 255, 0), inim.hitbox, 2)
            pygame.draw.rect(screen, (255, 255, 0), inim.rect, 2)

def criar_niveis():
    return {
        #'Hub': Niveis('mapas prontos\entrada.tmx', largura_tela, altura_tela),
        1: Niveis('mapas prontos/sala1.tmx', largura_tela, altura_tela), 
        2: Niveis('mapas prontos/sala2.tmx', largura_tela, altura_tela),
        3: Niveis('mapas prontos/sala3.tmx', largura_tela, altura_tela),
        4:Niveis('mapas prontos/sala4.tmx', largura_tela, altura_tela),
    }

fluxoDeJogo = Fluxo()

ObjetosNiveis = criar_niveis()
nivelAtual = 4
ObjNivel = ObjetosNiveis[nivelAtual]



def CarregarNivel(ObjNivel):
    Coletaveis = ObjNivel.grupo_colecionaveis

    # Inimigos
    Inimigos = ObjNivel.grupo_inimigos
    grupo_inimigos = pygame.sprite.Group()
    grupo_inimigos.add(Inimigos)

    grupo_colisao = pygame.sprite.Group()
    grupo_colisao.add(ObjNivel.grupo_colisao)

    

    return grupo_colisao, Inimigos, Coletaveis, grupo_inimigos

def irParaHub():
    global ObjNivel
    global nivelAtual
    if ObjNivel.player.mudarFase:
        nivelAtual = 'Hub'
        ObjNivel.player.mudarFase = False
    ObjNivel = ObjetosNiveis[nivelAtual]

while True:
    
    if fluxoDeJogo.start:
        fluxoDeJogo.telaDeStart(screen, fluxoDeJogo.lista_de_botoes[1], fluxoDeJogo.lista_de_botoes[0], fluxoDeJogo.lista_de_botoes, fluxoDeJogo.imagem_tela_start)
    
    if fluxoDeJogo.jogando:
        grupo_colisao, Inimigos, Coletaveis, grupo_inimigos = CarregarNivel(ObjNivel)
        fluxoDeJogo.jogo(ObjNivel.player, ObjNivel, grupo_colisao, Inimigos, Coletaveis, grupo_inimigos)
        irParaHub()
        if ObjNivel.player.vidas<=0:
            fluxoDeJogo.jogando = False
            fluxoDeJogo.derrotado = True
    
    if fluxoDeJogo.derrotado:
        fluxoDeJogo.telaDeGameOver()

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
        texto_pontuacao = fonte_grande.render(f"Pontos: {ObjNivel.player.pontuacao}", True, Cores.BRANCO)
        screen.blit(texto_pontuacao, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit