import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, window_height, window_width):
        super().__init__()
        self.window_height = window_height
        self.window_width = window_width
        #self.hp = 5
        #self.full_hp = 5
        #self.damage = 1
        #self.radius = 10
        #self.shots_fired = 0
        self.width, self.height = 50, 50

        #self.object_x, self.object_y = self.set_start_position(window_width, window_height)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 50)

    def set_start_position(self, window_width, window_height):
        dice = random.randint(0, 3)
        if dice == 0:
            object_y = random.randint(0, window_height)
            object_x = 0
        elif dice == 1:
            object_y = 0
            object_x = random.randint(0, window_width)
        elif dice == 2:
            object_y = random.randint(0, window_height)
            object_x = window_width
        elif dice == 3:
            object_y = window_height
            object_x = random.randint(0, window_width)

        return object_x, object_y

    def update(self):
        target_x = (self.window_width - self.width) // 2
        target_y = (self.window_height - self.height) // 2

        distance_x = target_x - self.rect.x
        distance_y = target_y - self.rect.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance == 0:
            return

        speed = 1
        direction_x = distance_x / distance
        direction_y = distance_y / distance

        self.rect.x += direction_x * speed
        self.rect.y += direction_y * speed