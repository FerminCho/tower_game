import math
import random


class enemy():
    hp = 5
    damage = 1
    circle_radius = 10
    circle_x = 0
    circle_y = 400
    circle_center = (circle_x, circle_y)

    def init(self, window_height, window_width):
        self.window_height = window_height
        self.window_width = window_width
        self.object_x, self.object_y = self.set_start_position(window_width, window_height)

    def set_start_position(self, window_width, window_height):
        dice = random.randint(0, 1)
        if dice == 0:
            object_y = random.randint(0, window_height)
            object_x = 0
        else:
            object_y = 0
            object_x = random.randint(0, window_width)

        return object_x, object_y

    def movement(self):
        target_x = (self.window_width - self.circle_radius) // 2
        target_y = (self.window_height - self.circle_radius) // 2

        distance_x = target_x - self.object_x
        distance_y = target_y - self.object_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        speed = 1
        if distance <= speed:
            return self.object_x, self.object_y

        # Calculate the direction vector (unit vector)
        direction_x = distance_x / distance
        direction_y = distance_y / distance

        self.object_x += direction_x * speed
        self.object_y += direction_y * speed

        return (self.object_x, self.object_y)