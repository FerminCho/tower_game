from game_data import GameData
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from enemies import Enemy
import math

class run():
    coins = 0
    round = 0
    def __init__(self):
        pass

class Round():
    def __init__(self, main_buttons, castle, layout, **kwargs):
        self.enemies = []
        self.bullets = []
        self.bullets_to_kill = {}
        self.main_buttons = main_buttons
        self.castle = castle
        self.towers = self.castle.towers_in_use
        self.layout = layout
        pass

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
            button.size = (0, 0)

    def end_round(self, dt):
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        for tower in self.towers.values():
            if tower[1]:
                Clock.unschedule(self.fire_bullet(dt, tower[1]))

        for enemy in self.enemies:
            self.layout.remove_widget(enemy)
        self.enemies = []

        for bullet in self.bullets:
            self.layout.remove_widget(bullet)
        self.bullets = []
        
        self.bullets_to_kill = {}

        for button in self.main_buttons:
            button.opacity = 1
            button.disabled = False
            button.size = (200, 100)


    def spawn_enemy(self, dt):
        enemy = Enemy()
        self.enemies.append(enemy)
        self.bullets_to_kill[enemy] = enemy.hp
        self.layout.add_widget(enemy)
    
    def fire_bullet(self, dt, tower):
        target_list = [enemy for enemy in self.bullets_to_kill]

        if bool(self.bullets_to_kill):  # Only fire if there are enemies
            bullet = tower.create_bullet(self.enemies)
            self.bullets.append(bullet)
            self.layout.add_widget(bullet)
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
            self.layout.remove_widget(bullet)
        if enemy in self.enemies and enemy.hp <= bullet.damage:
            self.enemies.remove(enemy)
            self.layout.remove_widget(enemy)
        else:
            enemy.hp -= bullet.damage

class shop():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_data = GameData()
    
    def shop_enteries(self):
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols = 2, spacing = 0, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (300, 300)

        entries = self.game_data.get_shop_entries()
        for entry in entries:
            button1 = Button(text=entry['name'], size_hint_y=None, height=40)
            button2 = Button(text=entry['price'], size_hint_y=None, height=40)
            grid_layout.add_widget(button1)
            grid_layout.add_widget(button2)
        popup_content.add_widget(grid_layout)
        popup = Popup(title='Shop Entries', content=popup_content, size_hint=(None, None), size=popup_size)
        popup.open()

    def buy():
        pass

    def upgrade():
        pass