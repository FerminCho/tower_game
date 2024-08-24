from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.animation import Animation
import random
import math
from movement import MovingObject

class Enemy(MovingObject):

    def __init__(self, **kwargs):
        self.size = (25, 25)
        target_pos = ((Window.width - self.width) / 2, (Window.height - self.height) / 2)
        self.set_start_position()
        super().__init__(start_pos=self.pos, target_pos=target_pos, color=(1, 0, 0, 1), size=(10, 10), speed=300)


    def set_start_position(self):
        # Generate a random starting position on one of the screen's edges
        edge = random.choice(['left', 'right', 'top', 'bottom'])

        if edge == 'left':
            self.pos = (-self.width, random.randint(0, Window.height - self.height))
        elif edge == 'right':
            self.pos = (Window.width, random.randint(0, Window.height - self.height))
        elif edge == 'top':
            self.pos = (random.randint(0, Window.width - self.width), Window.height)
        elif edge == 'bottom':
            self.pos = (random.randint(0, Window.width - self.width), -self.height) 