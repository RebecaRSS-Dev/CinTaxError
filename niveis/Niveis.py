import pygame
import pytmx
from entidades.Coletavel import Coletavel
from entidades.Inimigo import Inimigo
from entidades.Obstaculo import Obstacle

pygame.init()
class Niveis:
    def __init__(self, arquivo_tmx, player, largura_tela, altura_tela):
        self.mapa_tiled = pytmx.load_pygame(arquivo_tmx)

        map_altura_pixels_original = self.mapa_tiled.height * self.mapa_tiled.tileheight
        self.fator_escala = altura_tela / map_altura_pixels_original

        map_largura_pixels_escalada = (self.mapa_tiled.width * self.mapa_tiled.tilewidth) * self.fator_escala
        self.tile_width_escalado = self.mapa_tiled.tilewidth * self.fator_escala
        self.tile_height_escalado = self.mapa_tiled.tileheight * self.fator_escala

        self.offset_x = (largura_tela - map_largura_pixels_escalada) / 2
        self.offset_y = 0

        self.cache_tiles = {}
        self.grupo_colisao = self.criar_colisoes()

        self.portais = {}
        self.player_pos, inimigos, coletaveis, self.portais = self.carregar_objetos(self.mapa_tiled)
        
        largura_player = self.tile_width_escalado
        altura_player = self.tile_height_escalado

        if "Hub" in arquivo_tmx:
            largura_player *= 2
            altura_player *= 2

        self.player = player
        self.player.rect.center = self.player_pos
        self.grupo_inimigos = inimigos
        self.grupo_colecionaveis = coletaveis
        
        # Grupo que guardará APENAS os obstáculos de portais dinâmicos
        self.grupo_portais_obstaculos = pygame.sprite.Group()

    
    def carregar_objetos(self, tmx_data):
        player_start = (0, 0)
        inimigos = []
        coletaveis = []
        portais = {}

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
                    
                    # Identificar e criar os portais
                    if layer.name == "salas":
                        if obj.name.startswith("sala"):
                            portal_largura = 70
                            portal_altura = 45
                            portal_rect = pygame.Rect(0, 0, portal_largura, portal_altura)
                            portal_rect.center = (x, y)
                            portais[obj.name] = portal_rect

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
                    elif obj.name == "fragmento":
                        coletavel = Coletavel(x, y, 4)
                        coletaveis.append(coletavel)

        return player_start, inimigos, coletaveis, portais

    def desenhar_mapa(self,surface):
        for camada in self.mapa_tiled.visible_layers:
            if isinstance(camada, pytmx.TiledTileLayer):
                for x, y, gid in camada:
                    if gid == 0: continue
                    
                    tile_imagem = self.cache_tiles.get(gid)
                    if not tile_imagem:
                        imagem_original = self.mapa_tiled.get_tile_image_by_gid(gid)
                        if imagem_original:
                            dimensoes_escaladas = (int(self.tile_width_escalado), int(self.tile_height_escalado))
                            tile_imagem = pygame.transform.scale(imagem_original, dimensoes_escaladas)
                            self.cache_tiles[gid] = tile_imagem
                    
                    if tile_imagem:
                        pos_x = x * self.tile_width_escalado + self.offset_x
                        pos_y = y * self.tile_height_escalado + self.offset_y
                        surface.blit(tile_imagem, (pos_x, pos_y))

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