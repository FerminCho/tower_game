from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.label import Label
import random
import math

class Enemy(Widget):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.hp = 2
        self.damage = 1
        self.speed = 170
        self.value = 1
        self.perma_coins_value = 1
        self.direction = -math.pi / 2
        self.captured = False
        self.capturer = None
        self.shielded = False
        self.shield_hp = 0
        self.shield = None
        self.name = name

        self.rect_size = (25, 25)  # Size of the rectangle
        self.pos = (random.randint(0, Window.width - self.size[0]), Window.height)

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

        # Create a label to display text
        self.label = Label(text=self.name, size_hint=(None, None), size=self.rect_size, pos=self.pos, color=(1, 1, 1, 1))
        self.add_widget(self.label)

        # Bind the position and size of the label to the rectangle
        self.bind(pos=self.update_label, size=self.update_label)

    def update_label(self, *args):
        self.label.pos = self.pos
        self.label.size = self.rect_size

    def update(self, dt):
        if self.captured:
            self.change_movement(dt)
            return
        new_x = self.pos[0]
        new_y = self.pos[1] - self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos
        if self.shielded:
            self.update_shield()
            if self.shield_hp <= 0:
                self.remove_shield()

    
    def damage_taken(self, damage):
        if self.shielded:
            final_damage_taken = damage - self.shield_hp
            self.shield_hp -= damage
            if self.shield_hp <= 0:
                self.shield_hp = 0
        else:
            final_damage_taken = damage
        
        if final_damage_taken < 0:
            final_damage_taken = 0
        self.hp -= final_damage_taken
        return final_damage_taken
    
    def get_damage_taken(self, damage):
        if self.shielded:
            final_damage_taken = damage - self.shield_hp
        else:
            final_damage_taken = damage
        
        if final_damage_taken < 0:
            final_damage_taken = 0
        return final_damage_taken
    
    def get_damage_done(self):
        return self.damage
    
    def change_movement(self, dt):
        destination_x = self.capturer.pos[0] + self.capturer.rect_size[0] / 2 - self.rect_size[0] / 2
        destination_y = self.capturer.pos[1] + self.capturer.rect_size[1] / 2 - self.rect_size[1] / 2
        # Calculate the direction vector
        direction_x = destination_x - self.pos[0]
        direction_y = destination_y - self.pos[1]

        # Calculate the distance to the target
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Normalize the direction vector
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Update the position using the normalized direction vector
        new_x = self.pos[0] + direction_x * self.speed * dt
        new_y = self.pos[1] + direction_y * self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos
    
    def get_shield(self, shield_hp):
        self.shield_hp = shield_hp
        self.shielded = True
        self.bind(pos=self.update_shield, size=self.update_shield)
        with self.canvas.after:
            Color(0, 0, 1, 1)
            self.shield = Line(rectangle=(self.x, self.y, self.rect_size[0], self.rect_size[1]), width=2)
    
    def update_shield(self, *args):
        if self.shield:
            self.shield.rectangle = (self.x, self.y, self.rect_size[0], self.rect_size[1])
    
    def remove_shield(self):
        if self.shield:
            self.canvas.after.remove(self.shield)
            self.unbind(pos=self.update_shield, size=self.update_shield)
            self.shield = None
            self.shielded = False
            self.shield_hp = 0
    
    def remove_enemy(self):
        if self.shielded:
            self.remove_shield()
        self.parent.round.screen_enemies.remove(self)
        if self in self.parent.round.bullets_to_kill:
            del self.parent.round.bullets_to_kill[self]
        self.parent.remove_widget(self)

class ArmourEnemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.armour = 1
        self.name = "Armour Enemy"

    def damage_taken(self, damage):
        final_damage_taken = damage - self.armour
        self.hp -= final_damage_taken
        return final_damage_taken

    def get_damage_taken(self, damage):
        final_damage_taken = damage - self.armour
        return final_damage_taken
    
    def get_damage_done(self):
        return self.damage - self.armour

class FastEnemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 200
        self.name = "Fast Enemy"
