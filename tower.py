from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
import math

class Bullet(Widget):
    def __init__(self, rectangles, **kwargs):
        super().__init__(**kwargs)
        # Calculate target based on closest rectangle
        self.center_pos = (Window.width / 2, Window.height / 2)
        self.pos = self.center_pos
        self.rectangles = rectangles
        self.target_rect = None
        self.enemy = None
        self.find_closest_rectangle()
        self.size = (25, 25)

        with self.canvas:
            Color(1, 0, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        # Calculate velocity after setting the start position
        self.velocity = self.calculate_velocity()

        # Schedule the update with a slight delay
        Clock.schedule_once(self.start_moving, 0.1)
    
    def find_closest_rectangle(self):
        min_distance = float('inf')
        closest_rectangle = None
        closest_enemy = None

        for enemy in self.rectangles:
            # Calculate the center of the rectangle
            rect = enemy.rect

            rect_center = (
                rect.pos[0] + rect.size[0] / 2,
                rect.pos[1] + rect.size[1] / 2
            )

            # Calculate the Euclidean distance from the center of the screen
            distance = math.sqrt(
                (rect_center[0] - self.center_pos[0]) ** 2 +
                (rect_center[1] - self.center_pos[1]) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                closest_rectangle = rect
                closest_enemy = enemy

        self.target_rect = closest_rectangle
        self.enemy = closest_enemy

    def calculate_velocity(self):
        direction_x = self.target_rect.pos[0] - self.pos[0]
        direction_y = self.target_rect.pos[1] - self.pos[1]
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
        if self.check_collision():
            Clock.unschedule(self.update)
    
    def check_collision(self):
        return self.rect.pos.collide_widget(self.enemy)
    