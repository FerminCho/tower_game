from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
import math

class Tower(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fire_rate = 1
        self.damage = 1
        self.name = None
        #self.start_pos = 

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

class Bullet(Widget):
    def __init__(self, rectangles, **kwargs):
        super().__init__(**kwargs)
        self.damage = 1

        self.center_pos = (Window.width / 2, Window.height / 2)
        self.pos = self.center_pos
        self.rectangles = rectangles

        self.target_rect = None
        self.enemy = None
        self.find_closest_enemy()
        self.rect_size = (25, 25)

        with self.canvas:
            Color(1, 0, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)
        
        # Calculate velocity after setting the start position
        self.velocity = self.calculate_velocity()
    
    def find_closest_enemy(self):
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

    def update(self, dt):
        new_x = self.pos[0] + self.velocity[0] * dt
        new_y = self.pos[1] + self.velocity[1] * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos

        # Stop moving if the rectangle reaches the center
        if self.check_collision():
            Clock.unschedule(self.update)
    
    def check_collision(self):
        # Get the center of the bullet and enemy
        bullet_center = (
            self.pos[0] + self.rect_size[0] / 2,
            self.pos[1] + self.rect_size[1] / 2
        )
        enemy_center = (
            self.enemy.pos[0] + self.enemy.rect_size[0] / 2,
            self.enemy.pos[1] + self.enemy.rect_size[1] / 2
        )

        # Calculate the distance between the bullet and enemy
        distance = math.sqrt(
            (bullet_center[0] - enemy_center[0]) ** 2 +
            (bullet_center[1] - enemy_center[1]) ** 2
        )

        # Check if the distance is less than the sum of the radii (or half the widths)
        if distance < (self.rect_size[0] / 2 + self.enemy.rect_size[0] / 2):
            return True
        return False
    