import pygame

class Obstacle(pygame.sprite.Sprite):
    """ Classe simples para representar os obstáculos do mapa. """
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill((255, 0, 0, 100))
