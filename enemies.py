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
        self.size = (25, 25)

        with self.canvas:
            # Set the color and create a rectangle representing the enemy
            Color(1, 0, 0, 1)  # Red color
            self.rect = Rectangle(pos=self.set_start_position(), size=self.size)

        # Schedule the update method to move the enemy
        #Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.start_animation()

    def start_animation(self):
        # Calculate the center position of the screen
        center_x = (Window.width - self.width) / 2
        center_y = (Window.height - self.height) / 2

        # Create the animation to move the rectangle to the center
        animation = Animation(x=center_x, y=center_y, duration=5)  # Move to the center in x seconds
        animation.bind(on_progress=self.update_rectangle)

        # Start the animation
        animation.start(self)

    def update_rectangle(self, animation, widget, progress):
        # Update the rectangle position during the animation
        self.rect.pos = self.pos


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