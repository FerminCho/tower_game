from kivy.config import Config

# Set the window size using Config before importing Window
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
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
from resources import ResourceHandling
import random
import math

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.gmae_state = 'start window'
        self.enemies = []
        self.bullets = []
        self.bullets_to_kill = {}
        self.main_buttons = []
        self.castle = Castle()
        self.add_widget(self.castle)
        self.towers = self.castle.towers_in_use
        self.add_widget(self.castle.tower_layout)
        self.energy_layout()
        self.resource_layout()

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
        Clock.schedule_once(self.start, 0.01)

    
    def start(self, dt):
        self.gmae_state = 'game loop'
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.spawn_enemy, 3)
        Clock.schedule_once(self.end_round, 10)
        for tower in self.towers.values():
            if tower[1]:
                Clock.schedule_interval(lambda dt, t=tower[1]: self.fire_bullet(dt, t), tower[1].fire_rate)
        for button in self.main_buttons:
            button.opacity = 0
            button.disabled = True
            button.size = (0, 0)

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
            button.size = (200, 100)


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
        button_size = (40, 40)
        layout_big = BoxLayout(
                            orientation='horizontal',
                            spacing=(Window.width - 100 - button_size[0] * 4) / 3,
                            size_hint=(None, None), 
                            size=(Window.width, 60), 
                            pos=(0, Window.height * 0.2 - 84), 
                            padding=[50, 0]
                            )
        
        for i in range(4):
            self.energy_button = BorderButton(text='+', 
                                        size_hint=(None, None), 
                                        size=button_size,
                                        background_normal='',
                                        background_color=(0, 1, 0, 1),
                                        background_disabled_normal='',)
            
            self.energy_button.bind(on_press=self.energy_button.energy_handling)
            
            with self.energy_button.canvas:
                self.energy_button.rectangles = []
                for j in range(4):
                    color = Color(1, 0, 0, 1)
                    energy_rect = Rectangle(size=(button_size[0], 5))
                    self.energy_button.rectangles.append((color, energy_rect))
            
            self.energy_button.bind(pos=self.energy_button.update_rectangles)
            layout_big.add_widget(self.energy_button)
        
        self.add_widget(layout_big)

        toggle_button_size = (100, 50)
        toggle_button = ToggleButton(text='Energy +',
                                     size_hint=(None, None),
                                     size=toggle_button_size,
                                     pos=(Window.width - toggle_button_size[0], 0))
        self.energy_button.energy_state = 'add'
        toggle_button.bind(on_press=self.on_toggle)
        self.add_widget(toggle_button)
    
    def on_toggle(self, instance):
        if instance.state == 'down':
            self.energy_button.energy_state = 'remove'
            instance.text = 'Energy -'
        else:
            self.energy_button.energy_state = 'add'
            instance.text = 'Energy +'
    
    def resource_layout(self):
        resources = ResourceHandling()
        layout = BoxLayout(orientation='horizontal', 
                           size=(Window.width, 30), 
                           pos=(0, Window.height - 30),
                           spacing=10,
                           padding=10
                           )
        
        # Energy Label
        energy_label = Label(
            text='Energy: ' + str(resources.energy),
            size_hint=(None, None),
            font_size=Window.width * 0.025,
            pos=(0, Window.height - 30),
            color=(1, 1, 1, 1),
        )
        energy_label.bind(texture_size=lambda instance, value: instance.setter('size')(instance, value))
        layout.add_widget(energy_label)
        
        # Coins Label
        coins_label = Label(
            text='Coins: ' + str(resources.coins),
            size_hint=(None, None),
            font_size=Window.width * 0.025,
            pos=(energy_label.width, Window.height - 30),
            color=(1, 1, 1, 1),
        )
        coins_label.bind(texture_size=lambda instance, value: instance.setter('size')(instance, value))
        layout.add_widget(coins_label)
        
        self.add_widget(layout)

class BorderButton(Button):
    def __init__(self, **kwargs):
        super(BorderButton, self).__init__(**kwargs)
        #self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        line_width = 2
        self.canvas.after.clear()
        with self.canvas.after:
            Color(1, 0, 0, 1)  # Border color
            Line(rectangle=(self.x + line_width, self.y + line_width, self.width - line_width - 2, self.height - line_width - 2), width=line_width)  # Border width

    def update_rectangles(self, instance, value):
        for j, (color, rect) in enumerate(self.rectangles):
            rect.pos = (instance.pos[0], j * 10 + instance.pos[1] + 2)
    
    def energy_handling(self, instance):
        if self.energy_state == 'add':
            for color, rect in list(reversed(self.rectangles)):
                if color.rgba == [1, 0, 0, 1]:  # Check if the color is red
                    color.rgba = (1, 1, 1, 1)  # Change the color to white
                    break
        else:
            for color, rect in self.rectangles:
                if color.rgba == [1, 1, 1, 1]:  # Check if the color is red
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