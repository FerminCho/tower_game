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

        self.size = (25, 25)  # Size of the rectangle
        self.target_pos = (Window.width / 2, Window.height / 2)  # Center of the screen

        # Set the start position first
        self.set_start_position()

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Calculate velocity after setting the start position
        self.velocity = self.calculate_velocity()

        # Schedule the update with a slight delay
        Clock.schedule_once(self.start_moving, 0.1)

    def set_start_position(self):
        edge = random.choice(['left', 'right', 'top', 'bottom'])

        if edge == 'left':
            self.pos = (-self.size[0], random.randint(0, Window.height - self.size[1]))
        elif edge == 'right':
            self.pos = (Window.width, random.randint(0, Window.height - self.size[1]))
        elif edge == 'top':
            self.pos = (random.randint(0, Window.width - self.size[0]), Window.height)
        elif edge == 'bottom':
            self.pos = (random.randint(0, Window.width - self.size[0]), -self.size[1])

    def calculate_velocity(self):
        direction_x = self.target_pos[0] - self.pos[0]
        direction_y = self.target_pos[1] - self.pos[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        speed = 200  # Pixels per second
        velocity_x = (direction_x / distance) * speed
        velocity_y = (direction_y / distance) * speed

        return velocity_x, velocity_y

    def start_moving(self, dt):
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos

        # Stop moving if the rectangle reaches the center
        if math.isclose(new_x, self.target_pos[0], abs_tol=1) and math.isclose(new_y, self.target_pos[1], abs_tol=1):
            Clock.unschedule(self.update)
