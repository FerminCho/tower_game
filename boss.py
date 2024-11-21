from kivy.core.window import Window
from kivy.graphics import Rectangle, Line, Color
from kivy.clock import Clock
from kivy.uix.widget import Widget
from enemies import FastEnemy
import math

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
        self.enemy = None
        self.line = None

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

        self.absorb_unit(self.screen.screen_enemies)

        if self.enemy:
            #print(self.enemy.center)
            #print(self.center)
            if self.line:
                self.canvas.remove(self.line)
            with self.canvas:
                Color(1, 0, 0, 1)
                self.line = Line(points=[self.pos[0] + self.rect_size[0] / 2, self.pos[1] + self.rect_size[1] / 2, self.enemy.pos[0] + self.enemy.rect_size[0] / 2, self.enemy.pos[1]  + self.enemy.rect_size[1] / 2], width=2)
        else:
            if self.line:
                self.canvas.remove(self.line)
            self.line = None
    
    def damage_taken(self, damage):
        damage_done = damage
        self.hp -= damage_done
        return damage_done
    
    def get_damage_taken(self, damage):
        damage_done = damage
        return damage_done
    
    def absorb_unit(self, enemies):
        for enemy in enemies[1:]:
            if enemy.pos[1] + enemy.rect_size[1] < self.pos[1]:
                self.enemy = enemy
                enemy.capturer = self
                enemy.captured = True
            elif (self.center[0] - 15) <= enemy.center[0] <= (self.center[0] + 15) and (self.center[1] - 15) <= enemy.center[1] <= (self.center[1] + 15):
                enemies.remove(enemy)
                self.hp += enemy.hp * 2
                self.screen.layout.remove_widget(enemy)
                self.enemy = None
                print(self.hp)
