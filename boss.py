from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.widget import Widget
from enemies import FastEnemy
import math

class Boss1(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Boss1"
        self.hp = 100
        self.damage = 30
        self.direction = -math.pi / 2
        self.speed = 100

        self.rect_size = (50, 50)  # Size of the rectangle
        self.pos = (Window.width / 2 - self.rect_size[0] / 2 , Window.height)

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
        if self.hp <= 0:
            self.on_death()
    
    def on_death(self):
        fast_enemies = []
        for i in range(3):
            enemy = FastEnemy()
            enemy.pos = (self.pos[0] + i * 50, self.pos[1])
            fast_enemies.append(enemy)
        return fast_enemies