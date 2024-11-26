from kivy.core.window import Window
from kivy.graphics import Rectangle, Line, Color
from kivy.clock import Clock
from kivy.uix.widget import Widget
from enemies import FastEnemy
import math
import time

class Boss1(Widget):
    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.name = "Boss 1"
        self.hp = 10
        self.damage = 30
        self.direction = -math.pi / 2
        self.speed = 100
        self.value = 10
        self.perma_coins_value = 5
        self.dead = False

        self.rect_size = (50, 50)  # Size of the rectangle
        self.pos = (Window.width / 2 - self.rect_size[0] / 2 , Window.height)

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

    def start_moving(self, dt):
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        new_x = self.pos[0]
        new_y = self.pos[1] - self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos
    
    def on_death(self):
        self.dead = True
        for i in range(3):
            enemy = FastEnemy()
            enemy.pos = (self.pos[0] + i * 50, self.pos[1])
            self.screen.layout.add_widget(enemy)
            self.screen.enemies.append(enemy)
            self.screen.bullets_to_kill[enemy] = self.hp
    
    def damage_taken(self, damage):
        damage_done = damage
        self.hp -= damage_done
        return damage_done
    
    def get_damage_taken(self, damage):
        damage_done = damage
        return damage_done
    
    def damage_taken_check(self, damage): # Do i need this?
        damage_done = damage
        return damage_done

    def remove_enemy(self):
        self.parent.round.screen_enemies.remove(self)
        if self in self.parent.round.bullets_to_kill:
            del self.parent.round.bullets_to_kill[self]
        self.parent.remove_widget(self)

class Boss2(Widget):
    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.name = "Boss 2"
        self.hp = 10
        self.damage = 30
        self.direction = -math.pi / 2
        self.speed = 20
        self.value = 10
        self.perma_coins_value = 5
        self.enemy_line={}

        self.rect_size = (50, 50)  # Size of the rectangle
        self.pos = (Window.width / 2 - self.rect_size[0] / 2 , Window.height)

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

    def update(self, dt):
        new_x = self.pos[0]
        new_y = self.pos[1] - self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos

        for enemy in self.screen.screen_enemies[1:]:
            if enemy.pos[1] + enemy.rect_size[1] < self.pos[1] and not enemy.captured:
                if enemy not in self.enemy_line.keys():
                    enemy.capturer = self
                    enemy.captured = True
                    with self.canvas:
                        Color(1, 0, 0, 1)
                        line = Line(points=[self.pos[0] + self.rect_size[0] / 2, self.pos[1] + self.rect_size[1] / 2, enemy.pos[0] + enemy.rect_size[0] / 2, enemy.pos[1] + enemy.rect_size[1] / 2], width=2)
                    self.enemy_line[enemy] = line

        for enemy, line in self.enemy_line.copy().items():
            if (self.center[0] - 15) <= enemy.center[0] <= (self.center[0] + 15) and (self.center[1] - 15) <= enemy.center[1] <= (self.center[1] + 15):
                self.screen.screen_enemies.remove(enemy)
                self.hp += enemy.hp * 2
                self.screen.layout.remove_widget(enemy)
                self.canvas.remove(line)
                self.enemy_line.pop(enemy)
            else:
                self.redraw_line(enemy)
                
    
    def redraw_line(self, enemy):
        for line in self.enemy_line.values():
            self.canvas.remove(line)
            with self.canvas:
                Color(1, 0, 0, 1)
                line = Line(points=[self.pos[0] + self.rect_size[0] / 2, self.pos[1] + self.rect_size[1] / 2, enemy.pos[0] + enemy.rect_size[0] / 2, enemy.pos[1] + enemy.rect_size[1] / 2], width=2)
            self.enemy_line[enemy] = line
    
    def damage_taken(self, damage):
        damage_done = damage
        self.hp -= damage_done
        return damage_done
    
    def get_damage_taken(self, damage):
        damage_done = damage
        return damage_done
    
    def on_death(self):
        for enemy in self.screen.screen_enemies[1:]:
            enemy.captured = False

class Boss3(Widget):
    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.name = "Boss 3"
        self.hp = 10
        self.damage = 30
        self.direction = -math.pi / 2
        self.speed = 20
        self.value = 10
        self.perma_coins_value = 5
        self.shield_health = 1
        self.shield_skill_cooldown = 5
        self.last_shield_time = None

        self.rect_size = (25, 25)  # Size of the rectangle
        self.pos = (Window.width / 2 - self.rect_size[0] / 2 , Window.height)

        # Draw the rectangle at the start position
        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.pos, size=self.rect_size)

    def update(self, dt):
        new_x = self.pos[0]
        new_y = self.pos[1] - self.speed * dt
        self.pos = (new_x, new_y)
        self.rect.pos = self.pos

        current_time = time.time()
        if self.last_shield_time is None or (current_time - self.last_shield_time) >= self.shield_skill_cooldown:
            self.shield_enemy()
    
    def shield_enemy(self):
        for enemy in self.screen.screen_enemies[1:]:
            if not enemy.shielded:
                enemy.get_shield(self.shield_health)
                self.last_shield_time = time.time()
                return
    
    def damage_taken(self, damage):
        damage_done = damage
        self.hp -= damage_done
        return damage_done
    
    def get_damage_taken(self, damage):
        damage_done = damage
        return damage_done
    
    def remove_enemy(self):
        self.parent.round.screen_enemies.remove(self)
        if self in self.parent.round.bullets_to_kill:
            del self.parent.round.bullets_to_kill[self]
        self.parent.remove_widget(self)
