import math
import pygame


class Tower(pygame.sprite.Sprite):
    hp = 10
    dmg = 1
    fire_rate = 1000  # Fire every 1000 ms (1 second)
    last_shot_time = pygame.time.get_ticks()  # Track time of last shot
    width = 50
    height = 50

    def __init__(self, window_height, window_width):
        super().__init__()
        self.window_height = window_height
        self.window_width = window_width

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.window_width / 2, self.window_height / 2)

    def middle(self, enemy):
        target_x = (self.window_width) // 2
        target_y = (self.window_height) // 2
        distance_x = target_x - enemy.object_x
        distance_y = target_y - enemy.object_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        return distance

    def shoot(self, enemies):
        closest = None
        closest_distance = 0
        for enemy in enemies:
            distance = self.middle(enemy)
            if (distance < closest_distance or closest is None) and enemy.shots_fired != enemy.full_hp:
                closest = enemy
                closest_distance = distance
        bullet = Bullet(self.window_height, self.window_width, closest)
        return bullet




class Bullet(pygame.sprite.Sprite):
    radius = 3
    bullet_damage = 1
    width = 5
    height = 5


    def __init__(self, window_height, window_width, enemy):
        super().__init__()
        self.enemy = enemy
        self.window_height = window_height
        self.window_width = window_width
        self.position_x = (self.window_width - self.radius) // 2
        self.position_y = (self.window_height - self.radius) // 2

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.position_x, self.position_y)


    def update(self):
        target_x = self.enemy.object_x
        target_y = self.enemy.object_y

        distance_x = target_x - self.position_x
        distance_y = target_y - self.position_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        speed = 5

        if distance > speed:
            direction_x = distance_x / distance
            direction_y = distance_y / distance

            # Update floating-point position
            self.position_x += direction_x * speed
            self.position_y += direction_y * speed

            # Update rect position using integers for rendering
            self.rect.x = int(self.position_x)
            self.rect.y = int(self.position_y)

    def hit(self):
        self.enemy.hp = self.enemy.hp - self.bullet_damage