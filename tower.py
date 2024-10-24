from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
import math

class Tower(Widget):
    def __init__(self, fire_rate, damage, level, name, bullet_size, tower_pos, castle_pos, **kwargs):
        super().__init__(**kwargs)
        self.fire_rate = fire_rate
        self.level = level
        self.base_damage = damage
        self.damage = None
        self.name = name
        self.rect_size = (20, 20)
        self.tower_pos = tower_pos
        self.bullet_size = (bullet_size, bullet_size)
        self.castle_pos = castle_pos
        self.xp = 0
        self.rect = None

        self.bouncing_mod = False

        if self.bouncing_mod:
            self.mod = BouncingMod(self)

    def create_bullet(self, enemies):
        bullet_pos = (self.tower_pos[0] + self.rect_size[0] / 2, self.rect_size[1] / 2 + self.tower_pos[1])
        bullet = Bullet(enemies=enemies, 
                        damage=self.damage, 
                        fire_rate=self.fire_rate, 
                        bullet_pos=bullet_pos, 
                        size=self.bullet_size, 
                        castle_pos=self.castle_pos, 
                        tower=self)
        return bullet

    def draw_to_screen(self, tower_pos):
        if self.rect:
            self.canvas.remove(self.rect)
            self.rect = None
        self.tower_pos = tower_pos
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=((self.tower_pos[0] + self.rect_size[0] / 2), self.tower_pos[1] + self.rect_size[1] / 2), size=self.rect_size)

    def increment_xp(self, amount):
        self.xp += amount
        if self.xp >= 5 * self.level + 1:
            self.level_up()

    def level_up(self):
        self.xp = 0
        self.level += 1
        
        

class Bullet(Widget):
    def __init__(self, enemies, damage, fire_rate, bullet_pos, size, castle_pos, tower, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage
        self.fire_rate = fire_rate
        self.bullet_pos = bullet_pos
        self.enemies = enemies
        self.wall = castle_pos[1]
        self.velocity = (0, 0)
        self.tower = tower

        self.target_rect = None
        self.enemy = None
        self.rect_size = size

        with self.canvas:
            Color(1, 0, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.bullet_pos, size=self.rect_size)
        
        self.enemy = self.find_closest_enemy()
        self.calculate_velocity()
    
    def find_closest_enemy(self):
        min_distance = float('inf')
        closest_rectangle = None
        closest_enemy = None
        
        for enemy in self.enemies:
            # Calculate the center of the rectangle
            rect = enemy.rect

            distance = enemy.pos[1] - self.wall

            if distance < min_distance:
                min_distance = distance
                closest_rectangle = rect
                closest_enemy = enemy

        self.target_rect = closest_rectangle
        return closest_enemy

    def calculate_velocity(self):
        if not self.enemy:
            return
        
        speed = 300  # Pixels per second

        direction_x = self.enemy.pos[0] - self.bullet_pos[0]
        direction_y = self.enemy.pos[1] - self.bullet_pos[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        
        if distance == 0:
            self.velocity = (0, 0)
            return

        time_to_impact = distance / speed  # Assuming bullet speed is 600 pixels per second

        # Predict the enemy's future position
        future_enemy_pos = self.predict_enemy_position(time_to_impact)

        # Adjust the bullet's velocity to aim at the predicted future position
        direction_x = future_enemy_pos[0] - self.bullet_pos[0]
        direction_y = future_enemy_pos[1] - self.bullet_pos[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        self.velocity = (direction_x / distance) * speed, (direction_y / distance) * speed
    
    def predict_enemy_position(self, time_to_impact):
        # Assuming enemy is moving straight down
        future_x = self.enemy.pos[0] + self.enemy.rect_size[0] / 2
        future_y = self.enemy.pos[1] + self.enemy.rect_size[1] / 2 + self.enemy.speed * time_to_impact
        return future_x, future_y

    def update(self, dt):
        new_x = self.bullet_pos[0] + self.velocity[0] * dt
        new_y = self.bullet_pos[1] + self.velocity[1] * dt
        self.bullet_pos = (new_x, new_y)
        self.rect.pos = self.bullet_pos

        self.calculate_velocity()
    
    def check_collision(self):
        # Get the center of the bullet and enemy
        bullet_center = (
            self.bullet_pos[0] + self.rect_size[0] / 2,
            self.bullet_pos[1] + self.rect_size[1] / 2
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
    
class Mod():
    def __init__():
        pass

class BouncingBullet(Bullet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BouncingMod():
    def __init__(self, tower):
        self.tower = tower
    
    def bounce(self, bullet):
        if bullet.check_collision():
            enemies = self.round.enemies.remove(bullet.enemy)
            self.create_bullet(enemies, bullet.enemy)


    def create_bullet(self, enemies, start_enemy):
        bullet_pos = start_enemy.center
        bullet = Bullet(enemies=enemies, 
                        damage=self.tower.damage, 
                        fire_rate=self.tower.fire_rate, 
                        bullet_pos=bullet_pos, 
                        size=self.tower.bullet_size, 
                        castle_pos=self.tower.castle_pos, 
                        tower=self)
        return bullet