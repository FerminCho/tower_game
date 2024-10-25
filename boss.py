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
        self.name = "Boss1"
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
    
    def damage_taken_check(self, damage):
        damage_done = damage
        return damage_done

class Boss2(Widget):
    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.name = "Boss2"
        self.hp = 10
        self.damage = 30
        self.direction = -math.pi / 2
        self.speed = 100
        self.value = 10
        self.perma_coins_value = 5
        self.enemy = None

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

            if self.enemy:
                self.line.points = [self.pos[0], self.pos[1], self.enemy.pos[0], self.enemy.pos[1]]
        
        def damage_taken(self, damage):
            damage_done = damage
            self.hp -= damage_done
            return damage_done
        
        def absorb_unit(self, enemies):
            for enemy in enemies:
                if enemy.pos[1] < self.pos[1]:
                    enemies.remove(enemy)
                    self.hp += enemy.hp * 2
                    self.screen.layout.remove_widget(enemy)
                    self.enemy = enemy
                    return
                if enemy.center == self.center:
                    enemies.remove(enemy)
                    self.hp += enemy.hp * 2
                    self.screen.layout.remove_widget(enemy)
                    self.enemy = enemy
                    return
            pass

