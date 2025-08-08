import pygame

def carregar_frames(sprite_sheet_path, num_frames, frame_width, frame_height):
    sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, inicial):
        super().__init__()

        # Parâmetros da animação
        self.frames = carregar_frames("SpriteSheet-Inimigo.png", 6, 250, 250)
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 100  # ms entre frames

        self.image = self.frames[self.current_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = (x, y)

        # Hitbox menor
        hitbox_width, hitbox_height = 100, 100
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.center = self.rect.center

        self.movimentos = [
            pygame.Vector2(1, 0),
            pygame.Vector2(0, 1),
            pygame.Vector2(-1, 0),
            pygame.Vector2(0, -1)
        ]
        self.contador = inicial
        self.tempo = pygame.time.get_ticks()
        self.movimento = self.movimentos[self.contador]

    def patrulha(self, paredes, inimigos):
        tempoFinal = pygame.time.get_ticks()
        if (tempoFinal - self.tempo) >= 2000:
            self.tempo = tempoFinal
            self.contador += 1
            if self.contador > 3:
                self.contador = 0
            self.movimento = self.movimentos[self.contador]
        else:
            moviment = self.movimento * 2
            newPosition = self.rect.move(moviment)
            newHitbox = self.hitbox.copy()
            newHitbox.center = newPosition.center

            if any(newHitbox.colliderect(p.rect) for p in paredes) or any(newHitbox.colliderect(i.hitbox) for i in inimigos if i != self):
                self.contador += 2
                if self.contador > 3:
                    self.contador -= 4
                self.movimento = self.movimentos[self.contador]
                moviment = self.movimento * 2
                newPosition = self.rect.move(moviment)
                newHitbox = self.hitbox
                self.rect = newPosition
            else:
                if not any(newHitbox.colliderect(i.hitbox) for i in inimigos if i != self):
                    self.rect = newPosition

    def perseguir(self, player, paredes, inimigos):
        selfVector = pygame.Vector2(self.rect.center)
        vetorNormalizedPlayer = pygame.Vector2(player.rect.center)
        moviment = (vetorNormalizedPlayer - selfVector).normalize() * 4
        newPosition = self.rect.move(moviment)
        newHitbox = self.hitbox.copy()
        newHitbox.center = newPosition.center

        if not any(newHitbox.colliderect(p.rect) for p in paredes) and not newHitbox.colliderect(player.rect) and not any(newHitbox.colliderect(i.hitbox) for i in inimigos if i != self):
            self.rect = newPosition

    def move(self, player, paredes, inimigos):
        newHitbox = self.hitbox
        if self.rect.colliderect(player.rect):
            self.perseguir(player, paredes, inimigos)
        elif (not any(newHitbox.colliderect(p.rect) for p in paredes) and not newHitbox.colliderect(player.rect)):
            self.patrulha(paredes, inimigos)

    def update(self):
        # Atualiza hitbox
        self.hitbox.center = self.rect.center

        # Atualiza animação se estiver se movendo
        if self.movimento.length_squared() > 0:
            now = pygame.time.get_ticks()
            if now - self.animation_timer > self.animation_speed:
                self.animation_timer = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        else:
            self.image = self.frames[0]

    def draw(self, surface):
        self.image = pygame.transform.scale(self.image,(128,128))
        pos_x = self.rect.centerx - self.image.get_width() // 2
        pos_y = self.rect.centery - self.image.get_height() // 2
        surface.blit(self.image, (pos_x, pos_y))
