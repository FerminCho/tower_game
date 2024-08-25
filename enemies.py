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
        self.size = (25, 25)  # Correct size assignment
        self.set_start_position()  # Initialize position
        target_pos = ((Window.width - self.size[0]) / 2, (Window.height - self.size[1]) / 2)
        
        # Initialize the superclass with correct parameters
        super().__init__(start_pos=self.pos, target_pos=target_pos, color=(1, 0, 0, 1), size=self.size, speed=300)

    def set_start_position(self):
        # Generate a random starting position on one of the screen's edges
        edge = random.choice(['left', 'right', 'top', 'bottom'])

        if edge == 'left':
            self.pos = (-self.size[0], random.randint(0, Window.height - self.size[1]))
        elif edge == 'right':
            self.pos = (Window.width, random.randint(0, Window.height - self.size[1]))
        elif edge == 'top':
            self.pos = (random.randint(0, Window.width - self.size[0]), Window.height)
        elif edge == 'bottom':
            self.pos = (random.randint(0, Window.width - self.size[0]), -self.size[1])
