import pygame
import pytmx
from Inimigo import Inimigo
from Player import Player
pygame.init()

#Configuração Geral
screen = pygame.display.set_mode((1366, 768))

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
    def __init__(self,arquivo_tmx, largura_tela, altura_tela,inimigos,colecionaveis):
        self.mapa_tiled = pytmx.load_pygame(arquivo_tmx)

        # 1. CALCULAR FATOR DE ESCALA
        map_altura_pixels_original = self.mapa_tiled.height * self.mapa_tiled.tileheight
        self.fator_escala = altura_tela / map_altura_pixels_original

        # 2. CALCULAR NOVAS DIMENSÕES E OFFSET
        map_largura_pixels_escalada = (self.mapa_tiled.width * self.mapa_tiled.tilewidth) * self.fator_escala
        self.tile_width_escalado = self.mapa_tiled.tilewidth * self.fator_escala
        self.tile_height_escalado = self.mapa_tiled.tileheight * self.fator_escala

        self.offset_x = (largura_tela - map_largura_pixels_escalada) / 2
        self.offset_y = 0  # O mapa começa no topo da tela

        # Cache para armazenar imagens já redimensionadas e evitar trabalho repetido
        self.cache_tiles = {}

        #Criar os Grupos
        self.grupo_colisao = self.criar_colisoes()
        self.grupo_inimigos = inimigos
        self.grupo_colecionaveis = colecionaveis
        

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
        camadas_de_colisao = ['Collisions', 'Coast', 'Objects']

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

# Inicialização dos níveis
ObjetosNiveis ={1:Niveis('data\maps\grad1.tmx',largura_tela,altura_tela,[Inimigo(700,700,2),Inimigo(350,350,1)],[Coletavel(500, 600, 1), Coletavel(300, 500, 2)]),
                2:Niveis('data\maps\grad2.tmx',largura_tela,altura_tela,[],[])
                #3:Niveis('data\maps\grad3.tmx',largura_tela,altura_tela,[]),
                #4:Niveis('data\maps\grad4.tmx',largura_tela,altura_tela,[]),
}

NivelAtual = ObjetosNiveis[1]

player = Player()

paredes = []

Coletaveis = NivelAtual.grupo_colecionaveis

# Inimigos
Inimigos = NivelAtual.grupo_inimigos
grupo_inimigos = pygame.sprite.Group()
grupo_inimigos.add(Inimigos)

grupo_colisao = pygame.sprite.Group()
grupo_colisao.add(NivelAtual.grupo_colisao)

while True:
    teclasPressionadas = pygame.key.get_pressed()
    player.mover(teclasPressionadas,grupo_colisao,Inimigos)
    screen.fill(PRETO)
    NivelAtual.desenhar_mapa(screen)
    player.desenhar(screen)
    player.efeitos(Coletaveis)
    print(player.vidas)
    print(player.efeito)
    for coletavel in Coletaveis:
        coletavel.update()
        coletavel.desenhar(screen)
        pygame.draw.rect(screen, coletavel.cor, coletavel.rect,2)

    for inimigo in Inimigos:
        inimigo.move(player,grupo_colisao,Inimigos)
        inimigo.update()
        inimigo.draw(screen)

    pygame.draw.rect(screen,(255, 255, 0),player.rect,2)
    grupo_colisao.draw(screen)
    for inim in grupo_inimigos:
        pygame.draw.rect(screen, (0, 255, 0), inim.hitbox, 2)
        pygame.draw.rect(screen, (255, 255, 0), inim.rect, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    #pygame.display.flip()
    pygame.time.Clock().tick(60)