import math
import pygame


class Tower():
    hp = 10
    dmg = 1
    fire_rate = 1

    def init(self, window_height, window_width):
        self.window_height = window_height
        self.window_width = window_width

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
            if distance < closest_distance or closest is None:
                closest = enemy
                closest_distance = distance
        bullet = Bullet(self.window_height, self.window_width, closest)
        return bullet




class Bullet():
    radius = 1


    def init(self, window_height, window_width, enemy):
        self.enemy = enemy
        self.window_height = window_height
        self.window_width = window_width
        self.start_x = (self.window_width - self.radius) // 2
        self.start_y = (self.window_height - self.radius) // 2


    def move_bullet(self):
        target_x = self.enemy.object_x
        target_y = self.enemy.object_y

        distance_x = target_x - self.start_x
        distance_y = target_y - self.start_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        direction_x = distance_x / distance
        direction_y = distance_y / distance

        speed = 5

        self.start_x += direction_x * speed
        self.start_y += direction_y * speed

        return (self.start_x, self.start_y)