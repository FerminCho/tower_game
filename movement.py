from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.clock import Clock
import math

class MovingObject(Widget):
    def __init__(self, start_pos, target_pos, color, size, speed, **kwargs):
        super().__init__(**kwargs)
        
        # Ensure start_pos and target_pos are tuples or lists
        self.start_pos = list(start_pos)
        self.target_pos = list(target_pos)

        self.size_hint = (None, None)
        self.size = size
        self.speed = speed
        self.velocity = self.calculate_velocity()
        
        with self.canvas:
            Color(*color)
            self.rect = Rectangle(pos=self.start_pos, size=self.size)
        
        # Set position using Kivy's property
        self.pos = self.start_pos

    def calculate_velocity(self):
        direction_x = self.target_pos[0] - self.pos[0]
        direction_y = self.target_pos[1] - self.pos[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        velocity_x = (direction_x / distance) * self.speed
        velocity_y = (direction_y / distance) * self.speed
        return velocity_x, velocity_y

    def update(self, dt):
        # Update the position based on velocity
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos