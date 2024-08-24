from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
import math
from movement import MovingObject

class Bullet(MovingObject):
    def __init__(self, rectangles, **kwargs):
        # Calculate target based on closest rectangle
        self.center_pos = (Window.width / 2, Window.height / 2)
        self.rectangles = rectangles
        self.target_rect = self.find_closest_rectangle()
        
        target_pos = (self.target_rect.pos[0] + self.target_rect.size[0] / 2,
                      self.target_rect.pos[1] + self.target_rect.size[1] / 2)
        
        super().__init__(start_pos=self.center_pos, target_pos=target_pos, color=(1, 0, 0, 1), size=(10, 10), speed=300)
    
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

    