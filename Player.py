import pygame

class Player:
    def __init__(self,x,y):
        # Animação
        self.frames = self.carregar_frames("imagens/Sprites/ByteRightWalk.png", 2, 64, 64)
        self.frame_atual = 0
        self.tempo_animacao = pygame.time.get_ticks()
        self.velocidade_animacao = 120  # ms entre frames

        # Rect
        self.image = self.frames[self.frame_atual]
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 4

        #Definir o atributos inicais:
        self.vidas = 3
        self.efeito = None
        self.fragmentos = 0

    def carregar_frames(self, caminho, total_frames, largura, altura):
        sprite_sheet = pygame.image.load(caminho).convert_alpha()
        frames = []
        for i in range(total_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(0, i*altura, largura, altura))
            frames.append(frame)
        return frames

    def mover(self, teclas, paredes, inimigos):
        movimento = pygame.Vector2(0, 0)

        if teclas[pygame.K_LEFT]:
            movimento.x = -self.velocidade
            self.frames = self.carregar_frames("imagens/Sprites/ByteLeftWalk.png", 2, 64, 64)
            self.image = self.frames[self.frame_atual]
        elif teclas[pygame.K_RIGHT]:
            movimento.x = self.velocidade
            self.frames = self.carregar_frames("imagens/Sprites/ByteRightWalk.png", 2, 64, 64)
            self.image = self.frames[self.frame_atual]
        if teclas[pygame.K_UP]:
            movimento.y = -self.velocidade
            self.frames = self.carregar_frames("imagens/Sprites/ByteBackWalk.png", 2, 56, 56)
            self.image = self.frames[self.frame_atual]
        elif teclas[pygame.K_DOWN]:
            movimento.y = self.velocidade
            self.frames = self.carregar_frames("imagens/Sprites/ByteBackWalk.png", 2, 56, 56)
            self.image = self.frames[self.frame_atual]

        if movimento.length() != 0:
            movimento = movimento.normalize() * self.velocidade

            novo_rect = self.rect.move(movimento)

            if (not any(novo_rect.colliderect(p.rect) for p in paredes) and
                not any(novo_rect.colliderect(i.hitbox) for i in inimigos)):
                self.rect = novo_rect

            # Atualizar frame se estiver se movendo
            agora = pygame.time.get_ticks()
            if agora - self.tempo_animacao > self.velocidade_animacao:
                self.tempo_animacao = agora
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)
                self.image = self.frames[self.frame_atual]
                self.image = pygame.transform.scale(self.image,(40,40))
        else:
            # Parado = primeiro frame
            self.frame_atual = 0
            self.image = self.frames[0]
            self.image = pygame.transform.scale(self.image,(40,40))

    def coletar(self,coletaveis):
        for coletavel in coletaveis:
            if self.rect.colliderect(coletavel.rect) and self.efeito==None:
                self.tempo = pygame.time.get_ticks()
                coletaveis.remove(coletavel)
                return coletavel.tipo, coletavel.pontos
        return None, 0
    def efeitos(self,coletaveis):
        tipo, pontos = self.coletar(coletaveis)
        if tipo == None:
            if self.efeito=='velocidade':
                if pygame.time.get_ticks() - self.tempo > 5000:
                    self.velocidade = 4
                    self.efeito = None
            elif self.efeito=='invencibilidade':
                if pygame.time.get_ticks() - self.tempo > 5000:
                    self.efeito = None
        else:
            if tipo == 1 and pygame.time.get_ticks() - self.tempo < 5000:
                self.velocidade = 6
                self.efeito = 'velocidade'
            elif tipo == 2 and pygame.time.get_ticks() - self.tempo < 5000:
                self.efeito = 'invencibilidade'
            elif tipo == 3:
                pass
            elif tipo==4:
                self.fragmentos +=1

    def desenhar(self, superficie):
        self.image = pygame.transform.scale(self.image,(40,40))
        if self.efeito == 'invencibilidade':
            imagem_fantasma = self.image.copy()
            imagem_fantasma.set_alpha(128)
            self.image = imagem_fantasma
        superficie.blit(self.image, self.rect)
