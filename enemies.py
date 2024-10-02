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
        self.direction = -math.pi / 2

        self.rect_size = (25, 25)  # Size of the rectangle
        self.pos = (random.randint(0, Window.width - self.size[0]), Window.height)

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

    def start_moving(self, dt):
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        new_x = self.pos[0]
        new_y = self.pos[1] - self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos
    
    def damage_taken(self, damage):
        damage_done = damage
        self.hp -= damage_done
        return damage_done
    
    def get_damage_done(self):
        return self.damage

class ArmourEnemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.armour = 1

    def damage_taken(self, damage):
        damage_done = damage - self.armour
        self.hp -= damage_done
        return damage_done
    
    def get_damage_done(self):
        return self.damage - self.armour

class FastEnemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 400
