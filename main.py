from kivy.config import Config

# Set the window size using Config before importing Window
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from enemies import Enemy
from tower import Bullet
from castle import Castle
from game_data import GameData
from upgrade_window import UpgradeWindow
import random
import math

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.enemies = []
        self.bullets = []
        self.bullets_to_kill = {}
        self.main_buttons = []
        self.castle = Castle()
        self.add_widget(self.castle)
        self.towers = self.castle.towers_in_use
        self.add_widget(self.castle.tower_layout)
        self.energy_layout()

        # Create the start button
        self.start_button_size = (200, 100)
        self.start_button = Button(text="Start Game",
                                   size_hint=(None, None),
                                   size=self.start_button_size,
                                   pos=(Window.width / 2 - self.start_button_size[0] / 2, 0))
        self.start_button.bind(on_press=self.start_game)
        self.main_buttons.append(self.start_button)
        self.add_widget(self.start_button)

        # Add a button to switch to the UpgradeWindow
        upgrade_button = Button(text="Upgrade Tower",
                                size_hint=(None, None),
                                size=(200, 100),
                                pos=(0, 0))
        upgrade_button.bind(on_press=self.switch_to_upgrade)
        self.main_buttons.append(upgrade_button)
        self.add_widget(upgrade_button)

    def switch_to_upgrade(self, instance):
        self.manager.current = 'Upgrade'

    def start_game(self, instance):
        self.start_button.opacity = 0
        self.start_button.disabled = True    
        Clock.schedule_once(self.start, 0.01)

    
    def start(self, dt):
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_enemy, 3)
        Clock.schedule_once(self.end_round, 10)
        for tower in self.towers.values():
            if tower[1]:
                Clock.schedule_interval(lambda dt, t=tower[1]: self.fire_bullet(dt, t), tower[1].fire_rate)
        for button in self.main_buttons:
            button.opacity = 0
            button.disabled = True

    def end_round(self, dt):
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        for tower in self.towers.values():
            if tower[1]:
                Clock.unschedule(self.fire_bullet(dt, tower[1]))

        for enemy in self.enemies:
            self.remove_widget(enemy)
        self.enemies = []

        for bullet in self.bullets:
            self.remove_widget(bullet)
        self.bullets = []
        
        self.bullets_to_kill = {}
        self.start_button.opacity = 1
        self.start_button.disabled = False

        for button in self.main_buttons:
            button.opacity = 1
            button.disabled = False


    def spawn_enemy(self, dt):
        enemy = Enemy()
        self.enemies.append(enemy)
        self.bullets_to_kill[enemy] = enemy.hp
        self.add_widget(enemy)
    
    def fire_bullet(self, dt, tower):
        target_list = [enemy for enemy in self.bullets_to_kill]

        if bool(self.bullets_to_kill):  # Only fire if there are enemies
            bullet = tower.create_bullet(self.enemies)
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
            self.castle.detect_collision(enemy)
        
        if dt > 5:
            self.end_round()
            return

    def check_collision(self, bullet, enemy):
        # Get the center of the bullet and enemy
        bullet_center = (
            bullet.bullet_pos[0] + bullet.rect_size[0] / 2,
            bullet.bullet_pos[1] + bullet.rect_size[1] / 2
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

    def energy_layout(self):
        layout_big = BoxLayout(
                            orientation='horizontal',
                            spacing=(Window.width - 100 - 40 * 4) / 3,
                            size_hint=(None, None), 
                            size=(Window.width, 65), 
                            pos=(0, Window.height * 0.2 - 105), 
                            padding=[50, 0]
                            )
        
        for i in range(4):
            vertical_layout = BoxLayout(
                orientation='vertical',
                size_hint=(None, None),
                size=(40, 65)
            )

            energy_button = BorderButton(text='+', 
                                        size_hint=(None, None), 
                                        size=(40, 40),
                                        background_normal='',
                                        background_color=(0, 1, 0, 1),
                                        background_disabled_normal='',)
            
            energy_button.bind(on_press=energy_button.remove_energy)
            
            with energy_button.canvas:
                energy_button.rectangles = []
                for j in range(4):
                    color = Color(1, 0, 0, 1)
                    energy_rect = Rectangle(size=(40, 5))
                    energy_button.rectangles.append((color, energy_rect))
            
            energy_button.bind(pos=energy_button.update_rectangles)
            vertical_layout.add_widget(energy_button)
        
            add_energy_button = Button(text='+', 
                                        size_hint=(None, None), 
                                        size=(20, 20),
                                        background_normal='',
                                        background_color=(0, 1, 0, 1),
                                        background_disabled_normal='',)
            add_energy_button.bind(on_press=energy_button.add_energy)
            vertical_layout.add_widget(add_energy_button)
            layout_big.add_widget(vertical_layout)
        
        self.add_widget(layout_big)

class BorderButton(Button):
    def __init__(self, **kwargs):
        super(BorderButton, self).__init__(**kwargs)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Border color
            Line(rectangle=(self.x, self.y, self.width, self.height), width=2)  # Border width

    def update_rectangles(self, instance, value):
        for j, (color, rect) in enumerate(self.rectangles):
            rect.pos = (instance.pos[0], j * 10 + instance.pos[1] + 2)
    
    def remove_energy(self, instance):
        for color, rect in self.rectangles:
            if color.rgba == [1, 0, 0, 1]:  # Check if the color is red
                color.rgba = (0, 1, 0, 1)  # Change the color to green
                break
    
    def add_energy(self, instance):
        for color, rect in self.rectangles:
            if color.rgba == [0, 1, 0, 1]:  # Check if the color is red
                color.rgba = (1, 0, 0, 1)  # Change the color to green
                break
     
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlayWindow(name = 'Play'))
        sm.add_widget(UpgradeWindow(name = 'Upgrade'))
        return sm
        #return MyGame()

if __name__ == '__main__':
    MyApp().run()