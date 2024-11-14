from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.animation import Animation
import random
import math

class Enemy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hp = 2
        self.damage = 1
        self.speed = 200
        self.value = 1
        self.perma_coins_value = 1
        self.direction = -math.pi / 2
        self.captured = False
        self.capturer = None

        self.rect_size = (25, 25)  # Size of the rectangle
        self.pos = (random.randint(0, Window.width - self.size[0]), Window.height)

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

    def update(self, dt):
        if self.captured:
            self.change_movement(dt)
            return
        new_x = self.pos[0]
        new_y = self.pos[1] - self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos
    
    def damage_taken(self, damage):
        final_damage_taken = damage
        self.hp -= final_damage_taken
        return final_damage_taken
    
    def get_damage_taken(self, damage):
        final_damage_taken = damage
        return final_damage_taken
    
    def get_damage_done(self):
        return self.damage
    
    def change_movement(self, dt):
        # Calculate the direction vector
        direction_x = self.capturer.pos[0] - self.pos[0]
        direction_y = self.capturer.pos[1] - self.pos[1]

        # Calculate the distance to the target
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Normalize the direction vector
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Update the position using the normalized direction vector
        new_x = self.pos[0] + direction_x * self.speed * dt
        new_y = self.pos[1] + direction_y * self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos

class ArmourEnemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.armour = 1

    def damage_taken(self, damage):
        final_damage_taken = damage - self.armour
        self.hp -= final_damage_taken
        return final_damage_taken

    def get_damage_taken(self, damage):
        final_damage_taken = damage - self.armour
        return final_damage_taken
    
    def get_damage_done(self):
        return self.damage - self.armour

class FastEnemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 400
