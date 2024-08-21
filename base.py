import pygame
import math

class Base(pygame.sprite.Sprite):
    level = 3
    radius = 50

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height

        self.points = self.corner_points()
        self.image = pygame.Surface(self.get_bounding_rect_size(), pygame.SRCALPHA)

        adjusted_points = [(x - min(x for x, y in self.points), y - min(y for x, y in self.points)) for x, y in self.points]
        pygame.draw.polygon(self.image, (255, 0, 0), adjusted_points)
        self.rect = self.image.get_rect(center=(window_width/2, window_height/2))
        #self.rect.center = (window_width/2, window_height/2)

         # Adjust points to be relative to the top-left corner of the surface
        #self.relative_points = [(x - self.rect.x, y - self.rect.y) for x, y in self.points]
    
    def get_bounding_rect_size(self):
        """Calculate the size of the bounding rectangle that contains the polygon."""
        min_x = min(x for x, y in self.points)
        max_x = max(x for x, y in self.points)
        min_y = min(y for x, y in self.points)
        max_y = max(y for x, y in self.points)
        return (max_x - min_x, max_y - min_y)
    
    def check_collision(self, points, other_sprite):
        for x, y in points:
            pygame.draw.rect()
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
            x = self.radius * math.cos(angle_rad)
            y = self.radius * math.sin(angle_rad)

            # Append the vertex to the points list
            points.append((x, y))
        return points
    
    # Function to check if a point is inside a rectangle
    def point_in_rect(self, point, rect):
        return rect.collidepoint(point)

    # Function to check if two lines intersect (for edge-to-edge collision)
    def lines_intersect(self, p1, p2, q1, q2):
        # Using determinant and cross product to check for line intersection
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)
    
    # Function to check polygon collision with sprite
    def polygon_sprite_collision(self, polygon, sprite_rect):
        # Check if any point of the polygon is inside the sprite's rect
        for point in polygon:
            if self.point_in_rect(point, sprite_rect):
                return True

        # Check if any edge of the polygon intersects with any edge of the sprite's rect
        polygon_edges = [(polygon[i], polygon[(i+1) % len(polygon)]) for i in range(len(polygon))]
        rect_points = [sprite_rect.topleft, sprite_rect.topright, sprite_rect.bottomright, sprite_rect.bottomleft]
        rect_edges = [(rect_points[i], rect_points[(i+1) % len(rect_points)]) for i in range(4)]

        for poly_edge in polygon_edges:
            for rect_edge in rect_edges:
                if self.lines_intersect(poly_edge[0], poly_edge[1], rect_edge[0], rect_edge[1]):
                    return True

        return False
    

