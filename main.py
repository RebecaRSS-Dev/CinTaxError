import pygame
import pytmx
from Inimigo import Inimigo
from Player import Player
pygame.init()

#Configuração Geral
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

largura_tela, altura_tela = screen.get_size()

#Cores:
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CIANO = (0, 255, 255)
AMARELO = (255,255,0)
ROSA = (255, 0, 255)
BRANCO = (255, 255, 255)

#Fontes:
fonte_pequena = pygame.font.Font('ari-w9500-bold.ttf', 20)
fonte_pequena = pygame.font.Font('ari-w9500-bold.ttf', 36)

#classe botão
class Botao:
    def __init__(self, x, y, imagem_normal, imagem_selecionada):
        self.imagem_normal = imagem_normal
        self.imagem_selecionada = imagem_selecionada
        self.imagem_atual = self.imagem_normal 
        self.rect = self.imagem_normal.get_rect(center=(x, y))
    

    def checar_hover(self, posicao_mouse):
        if self.rect.collidepoint(posicao_mouse):
            self.imagem_atual = self.imagem_selecionada
        else:
            self.imagem_atual = self.imagem_normal
    
    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)


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
        screen.fill(PRETO)
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


class Obstacle(pygame.sprite.Sprite):
    """ Classe simples para representar os obstáculos do mapa. """
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill((255, 0, 0, 100))

#Classe coletaveis:
class Coletavel:
    def __init__(self, x, y, tipo):
        super().__init__()
        self.rect = pygame.Rect(x, y, 30, 30)
        self.tipo = tipo
        self.duracao_efeito = 0
        self.fragmentos = 0
        #analisar qual o tipo do coletavel:
        if self.tipo == 1:
            self.cor = AZUL
            self.pontos = 5
        else:
            self.duracao_efeito = 5000
            if self.tipo == 2:
                self.cor = VERDE
                self.pontos = 0
            elif self.tipo == 3:
                self.cor = CIANO
                self.pontos = 0
            elif self.tipo == 4:
                self.cor = AMARELO
                self.pontos = 0
        self.spritesheet = pygame.image.load("New Piskel.png").convert_alpha()
        self.frame_width = 32
        self.frame_height = 32
        self.columns = 3
        self.rows = 4
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

    def load_frames(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.spritesheet.subsurface((x, y, self.frame_width, self.frame_height))
                frames.append(frame)
        return frames

    def update(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    #desenhar:
    def desenhar (self, tela):
        tela.blit(self.image, self.rect.topleft)

# --- INÍCIO DAS MODIFICAÇÕES PARA ESCALA ---
class Niveis:
    def __init__(self, arquivo_tmx, largura_tela, altura_tela):
        self.mapa_tiled = pytmx.load_pygame(arquivo_tmx)

        # 1. Calcular fator de escala
        map_altura_pixels_original = self.mapa_tiled.height * self.mapa_tiled.tileheight
        self.fator_escala = altura_tela / map_altura_pixels_original

        # 2. Calcular dimensões escaladas
        map_largura_pixels_escalada = (self.mapa_tiled.width * self.mapa_tiled.tilewidth) * self.fator_escala
        self.tile_width_escalado = self.mapa_tiled.tilewidth * self.fator_escala
        self.tile_height_escalado = self.mapa_tiled.tileheight * self.fator_escala

        # Offsets para centralizar o mapa
        self.offset_x = (largura_tela - map_largura_pixels_escalada) / 2
        self.offset_y = 0

        # Cache para armazenar imagens já redimensionadas
        self.cache_tiles = {}

        # Criar grupo de colisões
        self.grupo_colisao = self.criar_colisoes()

        # Carregar objetos do mapa
        player_pos, inimigos, coletaveis = self.carregar_objetos(self.mapa_tiled)

        # Player escalado conforme tamanho do tile
        largura_player = self.tile_width_escalado
        altura_player = self.tile_height_escalado

        # Se for o mapa Hub, player é 2x maior
        if "Hub" in arquivo_tmx:
            largura_player *= 2
            altura_player *= 2

        self.player = Player(player_pos[0], player_pos[1], largura_player, altura_player)
        self.grupo_inimigos = inimigos
        self.grupo_colecionaveis = coletaveis
    
    def carregar_objetos(self, tmx_data):
        player_start = (0, 0)
        inimigos = []
        coletaveis = []

        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if not getattr(obj, "visible", True):
                        continue

                    # Corrigir posição com escala + offset
                    x = obj.x * self.fator_escala + self.offset_x
                    y = obj.y * self.fator_escala + self.offset_y

                    # Se for tile object, ajustar y para o topo do tile
                    if getattr(obj, "gid", None) is not None:
                        y = (obj.y - obj.height) * self.fator_escala + self.offset_y

                    # Player start (usar centro)
                    if obj.name == "player_start":
                        player_start = (x, y)

                    elif obj.name == "Player":
                        inimigo = Inimigo(0, 0)
                        inimigo.rect.center = (x, y)
                        inimigo.hitbox.center = inimigo.rect.center
                        inimigos.append(inimigo)

                    elif obj.name == "pontos":
                        coletavel = Coletavel(x, y, 1)
                        coletaveis.append(coletavel)

                    elif obj.name == "velocidade":
                        coletavel = Coletavel(x, y, 2)
                        coletaveis.append(coletavel)

                    elif obj.name == "invencibilidade":
                        coletavel = Coletavel(x, y, 3)
                        coletaveis.append(coletavel)

        return player_start, inimigos, coletaveis



    def desenhar_mapa(self,surface):
        for camada in self.mapa_tiled.visible_layers:
            if isinstance(camada, pytmx.TiledTileLayer):
                for x, y, gid in camada:
                    if gid == 0: continue # Pula tiles vazios
                    
                    tile_imagem = self.cache_tiles.get(gid)
                    if not tile_imagem:
                        # Se a imagem não está no cache, redimensiona e armazena
                        imagem_original = self.mapa_tiled.get_tile_image_by_gid(gid)
                        if imagem_original:
                            dimensoes_escaladas = (int(self.tile_width_escalado), int(self.tile_height_escalado))
                            tile_imagem = pygame.transform.scale(imagem_original, dimensoes_escaladas)
                            self.cache_tiles[gid] = tile_imagem
                    
                    if tile_imagem:
                        pos_x = x * self.tile_width_escalado + self.offset_x
                        pos_y = y * self.tile_height_escalado + self.offset_y
                        surface.blit(tile_imagem, (pos_x, pos_y))

    # 3. CRIAR COLISÕES COM A ESCALA APLICADA
    def criar_colisoes(self):
        grupo_colisao = pygame.sprite.Group()
        camadas_de_colisao = ['Collisions']

        for camada_nome in camadas_de_colisao:
            try:
                camada = self.mapa_tiled.get_layer_by_name(camada_nome)
                
                if isinstance(camada, pytmx.TiledTileLayer):
                    for x, y, gid in camada:
                        if gid:
                            rect_colisao = pygame.Rect(
                                x * self.tile_width_escalado + self.offset_x,
                                y * self.tile_height_escalado + self.offset_y,
                                self.tile_width_escalado,
                                self.tile_height_escalado
                            )
                            grupo_colisao.add(Obstacle(rect_colisao))
                
                elif isinstance(camada, pytmx.TiledObjectGroup):
                    for obj in camada:
                        if obj.visible:
                            rect_colisao = pygame.Rect(
                                obj.x * self.fator_escala + self.offset_x, 
                                obj.y * self.fator_escala + self.offset_y, 
                                obj.width * self.fator_escala, 
                                obj.height * self.fator_escala
                            )
                            grupo_colisao.add(Obstacle(rect_colisao))

            except ValueError:
                pass
        return grupo_colisao
        

# --- FIM DAS MODIFICAÇÕES PARA ESCALA ---
def criar_niveis():
    return {
        #'Hub': Niveis('mapas prontos\entrada.tmx', largura_tela, altura_tela),
        1: Niveis('mapas prontos\sala1.tmx', largura_tela, altura_tela), 
        2: Niveis('mapas prontos\sala2.tmx', largura_tela, altura_tela),
        3: Niveis('mapas prontos\sala3.tmx', largura_tela, altura_tela)
    }




fluxoDeJogo = Fluxo()

ObjetosNiveis = criar_niveis()
nivelAtual = 3
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
    
    
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)