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
        enemy = Enemy()
        self.add_widget(enemy)
        self.enemies.append(enemy)

        bullet = Bullet(self.enemies)
        self.add_widget(bullet)

        #Clock.schedule_interval(self.update, 1/60)  # Call update 60 times per second
    
    #def update(self, dt):
    #    for enemy in self.enemies:
    #        enemy.update(dt)

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