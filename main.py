from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from enemies import Enemy
from tower import Bullet
import random

Window.size = (800, 600)

class MyGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enemies = []
        self.bullets = []
        
        self.spawn_enemy()
        #self.spawn_bullet()

        Clock.schedule_interval(self.update, 1/60)
    
    def spawn_enemy(self):
        # Create multiple enemies
        for enemy in range(3):
            enemy = Enemy()
            self.enemies.append(enemy)
            self.add_widget(enemy)
    
    def spawn_bullet(self):
        # Create a bullet for each enemy
        for bullet in range(1):
            bullet = Bullet(rectangles=self.enemies)
            self.bullets.append(bullet)
            self.add_widget(bullet)

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)
        
        #for bullet in self.bullets:
        #    bullet.update(dt)
        #    
        #    for enemy in self.enemies:
        #        if bullet.collide_widget(enemy):
        #            #self.on_collision(bullet, enemy)
        #            print("hit")
        #            break

    def on_collision(self, bullet, enemy):
        print("Collision detected!")
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