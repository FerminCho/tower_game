from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from enemies import Enemy
from tower import Bullet
import random
import math

Window.size = (800, 600)

class MyGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemies = []
        self.bullets = []

        # Spawn enemies
        for _ in range(3):
            enemy = Enemy()
            self.enemies.append(enemy)
            self.add_widget(enemy)

        # Spawn bullets aimed at the first enemy
        if self.enemies:
            bullet = Bullet(rectangles=self.enemies)
            self.bullets.append(bullet)
            self.add_widget(bullet)

        Clock.schedule_once(self.start, 0.01)
    
    def start(self, dt):
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)

            for enemy in self.enemies:
                if self.check_collision(bullet, enemy):
                    print("Collision detected!")
                    self.on_collision(bullet, enemy)

        for enemy in self.enemies:
            enemy.update(dt)

    def check_collision(self, bullet, enemy):
        # Get the center of the bullet and enemy
        bullet_center = (
            bullet.pos[0] + bullet.rect_size[0] / 2,
            bullet.pos[1] + bullet.rect_size[1] / 2
        )
        enemy_center = (
            enemy.pos[0] + enemy.rect_size[0] / 2,
            enemy.pos[1] + enemy.rect_size[1] / 2
        )

        # Calculate the distance between the bullet and enemy
        distance = math.sqrt(
            (bullet_center[0] - enemy_center[0]) ** 2 +
            (bullet_center[1] - enemy_center[1]) ** 2
        )

        # Check if the distance is less than the sum of the radii (or half the widths)
        if distance < (bullet.rect_size[0] / 2 + enemy.rect_size[0] / 2):
            return True
        return False

    def on_collision(self, bullet, enemy):
        if bullet in self.bullets:
            self.bullets.remove(bullet)
            self.remove_widget(bullet)
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.remove_widget(enemy)  
        
class MyApp(App):
    def build(self):
        return MyGame()

if __name__ == '__main__':
    MyApp().run()