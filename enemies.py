from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
import random
import math

class Enemy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            # Set the color and create a rectangle representing the enemy
            Color(1, 0, 0, 1)  # Red color
            self.rect = Rectangle(pos=self.set_start_position(), size=(25, 25))

        # Schedule the update method to move the enemy
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        # Target position (center of the screen)
        target_x = Window.width / 2.0
        target_y = Window.height / 2.0

        # Calculate distance
        distance_x = target_x
        distance_y = target_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # Speed of movement
        speed = 1  # Floating-point speed

        # Move towards the target using floating-point precision
        if distance > speed:
            direction_x = distance_x / distance
            direction_y = distance_y / distance

            # Update floating-point position
            self.rect.pos = (self.rect.pos[0] + direction_x * speed, self.rect.pos[1] + direction_y * speed)

            # Update rect position using integers for rendering
            #self.rect.centerx = int(self.object_x)
            #self.rect.centery = int(self.object_y)

            # Update the widget's position to match the rectangle's position
            self.pos = self.rect.pos


    def set_start_position(self):
        dice = random.randint(0, 3)
        if dice == 0:
            object_y = random.randint(0, Window.height)
            object_x = 0
        elif dice == 1:
            object_y = 0
            object_x = random.randint(0, Window.width)
        elif dice == 2:
            object_y = random.randint(0, Window.height)
            object_x = Window.width
        elif dice == 3:
            object_y = Window.height
            object_x = random.randint(0, Window.width)

        return (object_x, object_y)