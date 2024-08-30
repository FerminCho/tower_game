from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from enemies import Enemy
from tower import Bullet
from castle import Castle
from game_data import GameData
import random
import math

Window.size = (800, 600)

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.enemies = []
        self.bullets = []
        self.bullets_to_kill = {}
        self.caslte = Castle()
        self.add_widget(self.caslte)

        # Create the start button
        self.start_button_size = (200, 100)
        self.start_button = Button(text="Start Game",
                                   size_hint=(None, None),
                                   size=self.start_button_size,
                                   pos=(Window.width / 2 - self.start_button_size[0] / 2, Window.height / 4))
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)
        print(self.start_button.pos)

    def start_game(self, instance):
        self.start_button.opacity = 0
        self.start_button.disabled = True    
        Clock.schedule_once(self.start, 0.01)

    
    def start(self, dt):
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_enemy, 3)
        Clock.schedule_interval(self.fire_bullet, 1)
        Clock.schedule_once(self.end_round, 20)

    def end_round(self, dt):
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        Clock.unschedule(self.fire_bullet)
        self.start_button.opacity = 1
        self.start_button.disabled = False


    def spawn_enemy(self, dt):
        enemy = Enemy()
        self.enemies.append(enemy)
        self.bullets_to_kill[enemy] = enemy.hp
        self.add_widget(enemy)
    
    def fire_bullet(self, dt):
        target_list = [enemy for enemy in self.bullets_to_kill]

        if bool(self.bullets_to_kill):  # Only fire if there are enemies
            bullet = Bullet(rectangles=target_list)
            self.bullets.append(bullet)
            self.add_widget(bullet)
            self.bullets_to_kill[bullet.enemy] -= bullet.damage
        
        for enemy in self.enemies:
            if enemy in self.bullets_to_kill and self.bullets_to_kill[enemy] <= 0:
                del self.bullets_to_kill[enemy]

    def update(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)

            for enemy in self.enemies:
                if self.check_collision(bullet, enemy):
                    self.on_collision(bullet, enemy)

        for enemy in self.enemies:
            enemy.update(dt)
            self.caslte.detect_collision(enemy)
        
        if dt > 5:
            self.end_round()
            return

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
        if enemy in self.enemies and enemy.hp <= bullet.damage:
            self.enemies.remove(enemy)
            self.remove_widget(enemy)
        else:
            enemy.hp -= bullet.damage

class StartWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlayWindow(name = 'Play'))
        return sm
        #return MyGame()

if __name__ == '__main__':
    MyApp().run()