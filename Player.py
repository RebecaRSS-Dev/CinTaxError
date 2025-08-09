import pygame

class Player:
    def __init__(self):
        # Animação
        self.frames = self.carregar_frames("imagens/Sprites/ByteRightWalk.png", 2, 64, 64)
        self.frame_atual = 0
        self.tempo_animacao = pygame.time.get_ticks()
        self.velocidade_animacao = 360  # ms entre frames

        # Rect
        self.image = self.frames[self.frame_atual]
        self.image = pygame.transform.scale(self.image,(25,25))
        self.rect = self.image.get_rect(center=(500, 500))
        self.velocidade = 6

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
            self.frames = self.carregar_frames("imagens/Sprites/ByteBackWalk.png", 2, 160, 160)
        elif teclas[pygame.K_DOWN]:
            movimento.y = self.velocidade
            self.frames = self.carregar_frames("imagens/Sprites/ByteDownWalk.png", 2, 64, 64)
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
                self.image = pygame.transform.scale(self.image,(52,52))
        else:
            # Parado = primeiro frame
            self.frame_atual = 0
            self.image = self.frames[0]
            self.image = pygame.transform.scale(self.image,(52,52))

    def desenhar(self, superficie):
        self.image = pygame.transform.scale(self.image,(52,52))
        superficie.blit(self.image, self.rect)
