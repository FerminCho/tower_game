from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.animation import Animation
from kivy.core.window import Window
import random
import math

class Bullet(Widget):
    def __init__(self, rectangles, **kwargs):
        super().__init__(**kwargs)
        self.rectangles = rectangles

        self.center_pos = (Window.width / 2, Window.height / 2)
        self.target_rect = self.find_closest_rectangle()
        self.bullet_size = (10, 10)
        
        with self.canvas:
            Color(1, 0, 0, 1)
            self.circle = Ellipse(pos=(self.center_pos[0] - self.bullet_size[0] / 2, 
                                        self.center_pos[1] - self.bullet_size[1] / 2), 
                                        size=self.bullet_size)
        
        self.pos = (self.center_pos[0] - self.bullet_size[0] / 2,
                    self.center_pos[1] - self.bullet_size[1] / 2)

        self.shoot_bullet()

    def shoot_bullet(self):
        target_pos = self.target_rect.pos

        # Calculate the direction vector
        direction_x = target_pos[0] + self.target_rect.size[0] / 2 - self.center_pos[0]
        direction_y = target_pos[1] + self.target_rect.size[1] / 2 - self.center_pos[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        speed = 500  # pixels per second
        duration = distance / speed

        # Create the animation towards the target
        animation = Animation(x=target_pos[0] + self.target_rect.size[0] / 2 - self.bullet_size[0] / 2, 
                              y=target_pos[1] + self.target_rect.size[1] / 2 - self.bullet_size[1] / 2, 
                              duration=duration)
        
        animation.bind(on_progress=self.update_circle_pos)
        animation.start(self)
    
    def update_circle_pos(self, animation, widget, progress):
        # Update the position of the Ellipse during the animation
        self.circle.pos = self.pos
    
    def find_closest_rectangle(self):
        min_distance = float('inf')
        closest_rectangle = None

        for rect in self.rectangles:
            # Calculate the center of the rectangle
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

        return closest_rectangle