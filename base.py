import pygame
import math

class Base(pygame.sprite.Sprite):
    hp = 1
    level = 3
    width = 100
    height = 100

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.center = (self.window_width/2, self.window_height/2)

    def check_collision(self, enemy_sprite):
        return self.rect.colliderect(enemy_sprite.rect)
    
