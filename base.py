import pygame
import math

class Base(pygame.sprite.Sprite):
    level = 3
    radius = 5

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height

        self.points = self.corner_points()
        self.image = pygame.Surface(self.get_bounding_rect_size(), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 0, 0), self.points)
        self.rect = self.image.get_rect(center=self.center)

         # Adjust points to be relative to the top-left corner of the surface
        self.relative_points = [(x - self.rect.x, y - self.rect.y) for x, y in self.points]
    
    def get_bounding_rect_size(self):
        """Calculate the size of the bounding rectangle that contains the polygon."""
        min_x = min(x for x, y in self.points)
        max_x = max(x for x, y in self.points)
        min_y = min(y for x, y in self.points)
        max_y = max(y for x, y in self.points)
        return (max_x - min_x, max_y - min_y)
    
    def check_collision(self, other_sprite):
        # Override collision check
        return self.rect.colliderect(other_sprite.rect) and self.point_in_polygon(self.relative_points, other_sprite.rect.center)

    def corner_points(self):
        num_sides = self.level
        angle_between_vertices = 360 / num_sides

        # List to store the polygon's vertex positions
        points = []

        for i in range(num_sides):
            # Convert the angle to radians
            angle_rad = math.radians(i * angle_between_vertices)

            # Calculate the x and y coordinates of each vertex
            x = self.window_width / 2 + self.radius * math.cos(angle_rad)
            y = self.window_height / 2 + self.radius * math.sin(angle_rad)

            # Append the vertex to the points list
            points.append((x, y))
        return points
    
    @staticmethod
    def point_in_polygon(poly, point):
        """Check if a point is inside the polygon."""
        x, y = point
        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside
    

