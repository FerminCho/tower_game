from game_data import GameData
from tower import Tower
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from enemies import Enemy, FastEnemy, ArmourEnemy
from castle import Castle
import math
import random
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from boss import Boss1
import threading

class run(EventDispatcher):
    coins = NumericProperty(0)
    round = NumericProperty(0)
    skill_points = NumericProperty(0)
    energy = NumericProperty(0)
    hp = NumericProperty(0)
    def __init__(self, home, **kwargs):
        self.home = home
        self.coins = 0 + self.home.extra_coins
        self.round = 5
        self.skill_points = 0 + self.home.extra_skill_points
        self.castle = Castle(self)
        self.energy = self.castle.base_energy + self.home.extra_energy
        self.hp = self.castle.base_hp + self.home.extra_hp
        self.energy_buttons = None
        self.game_data = GameData()
        self.unlocked_towers = self.game_data.get_unlocked_towers()
        self.towers = self.game_data.get_all_towers()
        self.tower_instances = []
        for tower_name in self.unlocked_towers:
            for tower in self.towers:
                if tower['name'] == tower_name:
                    full_tower = Tower(fire_rate=tower['fire_rate'], 
                                       damage=tower['damage'], level=0, 
                                       name=tower['name'], 
                                       bullet_size=tower['size'], 
                                       tower_pos=None, 
                                       castle_pos=self.castle.rect_pos)
                    self.tower_instances.append(full_tower)
    
    def save_run(self):
        data = {
            'coins': self.coins,
            'round': self.round,
            'skill_points': self.skill_points,
            'energy': self.energy,
            'hp': self.hp,
            'towers': []
        }
        for tower in self.tower_instances:
            data['towers'].append({
                'fire_rate': tower.fire_rate,
                'damage': tower.base_damage,
                'level': tower.level,
                'name': tower.name,
                'bullet_size': tower.bullet_size,
                'tower_pos': tower.tower_pos,
                'castle_pos': tower.castle_pos
            })

        self.game_data.save_run(data)

class Round():
    def __init__(self, main_buttons, castle, layout, run, **kwargs):
        self.enemies = []
        self.bullets = []
        self.bullets_to_kill = {}
        self.run = run
        self.main_buttons = main_buttons
        self.castle = castle
        self.towers = self.castle.towers_in_use
        self.layout = layout
        self.schedule_events = []
        self.gamedata = GameData()  
        self.round_enemies = []
        self.boss = None 
    
    def populate_enemies(self):
        for entry in self.gamedata.get_enemies_per_round():
            current_round_enemies = None
            if entry['round'] == self.run.round:
                current_round_enemies = entry
                break
        for i in range (current_round_enemies['normal_enemies']):
            self.round_enemies.append(Enemy())
        for i in range (current_round_enemies['fast_enemies']):
            self.round_enemies.append(FastEnemy())
        for i in range (current_round_enemies['armor_enemies']):
            self.round_enemies.append(ArmourEnemy())
        random.shuffle(self.round_enemies)

        if current_round_enemies['boss'] != "None":
            if current_round_enemies['boss'] == "Boss 1":
                self.boss = Boss1(self)
            elif current_round_enemies['boss'] == "Boss2":
                #self.boss = Boss2()
                pass
            elif current_round_enemies['boss'] == "Boss3":    
                #self.boss = Boss3()
                pass

    def start(self, dt):
        self.populate_enemies()
        for button in self.main_buttons:
            button[0].opacity = 0
            button[0].disabled = True
            button[0].size = (0, 0)
            button[0].size_hint = (None, None)
        self.schedule_events.append(Clock.schedule_interval(self.update, 1/60))
        self.schedule_events.append(Clock.schedule_interval(self.spawn_enemy, 3))
        
        for tower in self.towers.values():
            if tower[1]:
                event = Clock.schedule_interval(lambda dt, t=tower[1]: self.fire_bullet(dt, t), tower[1].fire_rate)
                self.schedule_events.append(event)

    def end_round(self, dt):
        for event in self.schedule_events:
            Clock.unschedule(event)
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
            button[0].opacity = 1
            button[0].disabled = False
            button[0].size_hint = (button[1], 1)


    def spawn_enemy(self, dt):
        if len(self.round_enemies) == 0:
            return
        enemy = self.round_enemies[0]
        self.enemies.append(enemy)
        self.bullets_to_kill[enemy] = enemy.hp
        self.layout.add_widget(enemy)
        self.round_enemies.pop(0)
    
    def fire_bullet(self, dt, tower):

        for i in range(4):
            if self.towers[i][1] == tower and self.run.energy_buttons[i][1] <= 0:
                return
            elif self.towers[i][1] == tower:
                tower.damage = tower.base_damage * (0.5 + 0.5 * self.run.energy_buttons[i][1])

        if bool(self.bullets_to_kill):  # Only fire if there are enemies
            bullet = tower.create_bullet(self.enemies)
            if bullet.enemy in self.bullets_to_kill:
                self.bullets.append(bullet)
                self.layout.add_widget(bullet)
                self.bullets_to_kill[bullet.enemy] -= bullet.enemy.damage_taken(bullet.damage)
        
                if self.bullets_to_kill[bullet.enemy] <= 0:
                    del self.bullets_to_kill[bullet.enemy]

        self.bullets_to_kill = {enemy: hp for enemy, hp in self.bullets_to_kill.items() if hp > 0}

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)
            self.castle.detect_collision(enemy)

        if len(self.round_enemies) == 0 and not self.enemies:
            if self.boss:
                self.enemies.append(self.boss)
                self.bullets_to_kill[self.boss] = self.boss.hp
                self.layout.add_widget(self.boss)
            else:    
                self.run.round += 1
                self.end_round(dt)
                return

        for bullet in self.bullets:
            bullet.update(dt)

            for enemy in self.enemies:
                if self.check_collision(bullet, enemy):
                    self.on_collision(bullet, enemy)

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
        if enemy in self.enemies and enemy.hp <= bullet.damage: # Fix this so it work with armored enemies enemy.damage_taken_ceck(bullet.damage)
            self.enemies.remove(enemy)
            self.layout.remove_widget(enemy)
            self.run.coins += enemy.value
            if bullet.tower.level <= 6:
                bullet.tower.increment_xp(enemy.hp)
            for bullet in self.bullets:
                if bullet.enemy == enemy:
                    self.bullets.remove(bullet)
                    self.layout.remove_widget(bullet)
            if self.boss and self.boss.hp <= 0:
                self.boss.on_death()
                self.boss = None
        else:
            hp_loss = enemy.damage_taken(bullet.damage)
            if bullet.tower.level <= 6:
                bullet.tower.increment_xp(hp_loss)

class shop():
    def __init__(self, run, castle, **kwargs):
        #super().__init__(**kwargs)
        self.game_data = GameData()
        self.run = run
        self.castle = castle
    
    def shop_enteries(self, instance):
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols = 2, spacing = 0, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (Window.width * 0.8, Window.height * 0.8)

        entries = self.game_data.get_shop_entries()
        for entry in entries:
            button1 = Button(text=entry['name'], size_hint_y=None, height=40)
            button2 = Button(text=str(entry['price']), size_hint_y=None, height=40)
            button2.bind(on_release=lambda btn, name=entry['name'], price=entry['price']: self.buy(name, price))
            grid_layout.add_widget(button1)
            grid_layout.add_widget(button2)
        popup_content.add_widget(grid_layout)
        popup = Popup(title='Shop Entries', content=popup_content, size_hint=(None, None), size=popup_size)
        popup.open()

    def buy(self, name, price):
        if self.run.coins < price:
            return
        else:
            self.run.coins -= price

        match name:
            case "1 Energy":
                self.run.energy += 1
                return
            case "1 HP":
                self.run.hp += 1
                return
            case "1 Skill Point":
                self.run.skill_points += 1
                return
        
        for tower in self.game_data.get_unlocked_towers():
            if tower == name:
                self.game_data.unlock_tower(name)
                return

    def upgrade():
        pass