from game_data import GameData
from tower import Tower, burst_fire_tower, Sniper_tower
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
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
from boss import Boss1, Boss2, Boss3
import threading

class run(EventDispatcher):
    coins = NumericProperty(0)
    round = NumericProperty(0)
    skill_points = NumericProperty(0)
    energy = NumericProperty(0)
    hp = NumericProperty(0)
    def __init__(self, **kwargs):
        self.home = None # Needs to wait for creation of home screen
        self.play_window = None # Needs to wait for creation of play screen
        self.upgrade_window = None # Needs to wait for creation of upgrade screen
        self.energy_buttons = None
        self.castle = Castle(self)
        self.game_data = GameData()
        self.existing_run = self.game_data.get_existing_run()['saved']
        self.towers = self.game_data.get_all_towers()
        self.tower_instances = []
    
    def start_run(self):
        if self.existing_run:
            self.load_run()
        else:
            self.new_run()
    
    def load_run(self):
        data = self.game_data.load_run()
        self.coins = data['coins']
        self.perma_coins = data['perma_coins']
        self.round = data['round']
        self.skill_points = data['skill_points']
        self.energy = data['energy']
        self.hp = data['hp']
        self.towers = self.game_data.get_all_towers()
        self.unlocked_towers = self.game_data.get_unlocked_towers()
        self.energy_buttons = self.play_window.get_energy_buttons()

        for tower in data['towers']: # Fix this part to work with a variety of tower classes
            full_tower = Tower(fire_rate=tower['fire_rate'], 
                               damage=tower['damage'], level=tower['level'], 
                               name=tower['name'], 
                               bullet_size=tower['bullet_size'], 
                               tower_pos=tower['tower_pos'], 
                               castle_pos=tower['castle_pos'])
            full_tower.xp = tower['xp']
            self.tower_instances.append(full_tower)
    
    def save_run(self):
        data = {
            'coins': self.coins,
            'perma_coins': self.perma_coins,
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
                'castle_pos': tower.castle_pos,
                'xp': tower.xp
            })

        self.game_data.save_run(data)
    
    def new_run(self):
        self.coins = 0 + self.home.extra_coins
        self.round = 6
        self.skill_points = 1 + self.home.extra_skill_points
        self.perma_coins = 0
        self.energy = self.castle.base_energy + self.home.extra_energy
        self.hp = self.castle.base_hp + self.home.extra_hp
        self.unlocked_towers = self.game_data.get_unlocked_towers()
        self.energy_buttons = self.play_window.get_energy_buttons()
        self.upgrade_window.reset_upgrades()

        for tower_name in self.unlocked_towers:
            for tower in self.towers:
                if tower['name'] == 'Burst Tower' and tower_name == 'Burst Tower':
                    full_tower = burst_fire_tower(fire_rate=tower['fire_rate'], 
                                       damage=tower['damage'], 
                                       level=0, 
                                       name=tower['name'], 
                                       bullet_size=tower['size'], 
                                       tower_pos=None, 
                                       castle_pos=self.castle.rect_pos,
                                       base_burst_bullets=tower['base_burst_bullets'],
                                       extra_burst_bullets=tower['extra_burst_bullets'])
                    self.tower_instances.append(full_tower)
                elif tower['name'] == "Sniper Tower" and tower_name == "Sniper Tower":
                    full_tower = Sniper_tower(fire_rate=tower['fire_rate'], 
                                       damage=tower['damage'], 
                                       level=0, 
                                       name=tower['name'], 
                                       bullet_size=tower['size'], 
                                       tower_pos=None, 
                                       castle_pos=self.castle.rect_pos,)
                    self.tower_instances.append(full_tower)
                elif tower['name'] == tower_name and tower['name'] != "Burst Tower":
                    full_tower = Tower(fire_rate=tower['fire_rate'], 
                                       damage=tower['damage'], 
                                       level=0, 
                                       name=tower['name'], 
                                       bullet_size=tower['size'], 
                                       tower_pos=None, 
                                       castle_pos=self.castle.rect_pos)
                    self.tower_instances.append(full_tower)
        
        for entry in self.game_data.get_shop_entries():
            entry['times_bought'] = 0



class Round():
    def __init__(self, main_buttons, castle, layout, run, **kwargs):
        self.screen_enemies = []
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
            self.round_enemies.append(Enemy("Basic Enemy"))
        for i in range (current_round_enemies['fast_enemies']):
            self.round_enemies.append(Enemy("Fast Enemy"))
        for i in range (current_round_enemies['armor_enemies']):
            self.round_enemies.append(Enemy("Armour Enemy"))
        random.shuffle(self.round_enemies)

        if current_round_enemies['boss'] != "None":
            if current_round_enemies['boss'] == "Boss 1":
                self.boss = Boss1(self)
            elif current_round_enemies['boss'] == "Boss 2":
                self.boss = Boss2(self)
                self.round_enemies.insert(0, self.boss)
            elif current_round_enemies['boss'] == "Boss 3":    
                self.boss = Boss3(self)
                self.round_enemies.insert(0, self.boss)
        else:
            self.boss = None

    def start(self, dt):
        self.populate_enemies()
        for button in self.main_buttons:
            button[0].opacity = 0
            button[0].disabled = True
            button[0].size = (0, 0)
            button[0].size_hint = (None, None)
        self.schedule_events.append(Clock.schedule_interval(self.update, 1/60))
        self.schedule_events.append(Clock.schedule_interval(self.spawn_enemy, 1))
        
        for tower in self.towers:
            if tower[1]:
                event = Clock.schedule_interval(lambda dt, t=tower[1]: self.fire_bullet(dt, t), tower[1].fire_rate)
                self.schedule_events.append(event)
                tower[1].enemies = self.screen_enemies

    def end_round(self, dt):
        for event in self.schedule_events:
            Clock.unschedule(event)
        for tower in self.towers:
            if tower[1]:
                Clock.unschedule(self.fire_bullet(dt, tower[1]))
            if tower[1] and tower[1].name == "Burst Tower":
                tower[1].ultimate_used = False

        for enemy in self.screen_enemies:
            self.layout.remove_widget(enemy)
        self.screen_enemies = []

        for bullet in self.bullets:
            self.layout.remove_widget(bullet)
        self.bullets = []
        
        self.bullets_to_kill = {}

        for button in self.main_buttons:
            button[0].opacity = 1
            button[0].disabled = False
            button[0].size_hint = (button[1], 1)

    def end_run(self, dt):
        self.end_round(dt)

        self.layout.manager.current = 'Home'

    def spawn_enemy(self, dt):
        if len(self.round_enemies) == 0:
            return
        enemy = self.round_enemies[0]
        self.screen_enemies.append(enemy)
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
            bullet = tower.create_bullet(self.screen_enemies)
            if bullet is not None and bullet.enemy in self.bullets_to_kill:
                self.bullets.append(bullet)
                self.layout.add_widget(bullet)
                self.bullets_to_kill[bullet.enemy] -= bullet.enemy.get_damage_taken(bullet.damage)
        
                if self.bullets_to_kill[bullet.enemy] <= 0:
                    del self.bullets_to_kill[bullet.enemy]

        self.bullets_to_kill = {enemy: hp for enemy, hp in self.bullets_to_kill.items() if hp > 0}

    def update(self, dt):
        if self.run.hp <= 0:
            self.run.home.perma_coins += self.run.perma_coins
            self.end_run(dt)
            return

        if len(self.round_enemies) == 0 and not self.screen_enemies:
            if self.boss and self.boss.name == "Boss 1":
                self.screen_enemies.append(self.boss)
                self.bullets_to_kill[self.boss] = self.boss.hp
                self.layout.add_widget(self.boss)
            else:    
                self.run.round += 1
                self.end_round(dt)
                return
        
        for enemy in self.screen_enemies:
            enemy.update(dt)
            self.castle.detect_collision(enemy)

        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.check_collision():
                bullet.on_collision(self)

class shop():
    def __init__(self, run, castle, **kwargs):
        self.game_data = GameData()
        self.run = run
        self.castle = castle
    
    def shop_enteries(self, instance):
        popup_size = (Window.width * 0.8, Window.height * 0.8)
        
        # Ensure FloatLayout fills the Popup content area
        popup_content = FloatLayout(size_hint=(1, 1))
        
        grid_layout = GridLayout(cols=2, spacing=0, size_hint=(1, None))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        grid_layout.height = len(self.game_data.get_shop_entries()) * 40  # Adjust height based on entries

        entries = self.game_data.get_shop_entries()
        for entry in entries:
            button1 = Button(text=entry['name'], size_hint_y=None, height=40)
            if entry['times_bought'] == entry['max_times_bought']:
                button2= Button(text="Maxed", size_hint_y=None, height=40)
                button2.disabled = True
            else:
                button2 = Button(text=str(entry['price']), size_hint_y=None, height=40)
                button2.bind(on_release=lambda btn, entry=entry, price=entry['price']: self.buy_stat(btn, entry, price))
            grid_layout.add_widget(button1)
            grid_layout.add_widget(button2)
        
        # Wrap the GridLayout in a ScrollView to ensure it fits within the Popup
        scroll_view = ScrollView(size_hint=(1, 0.9), pos_hint={'x': 0, 'y': 0.1})
        scroll_view.add_widget(grid_layout)
        popup_content.add_widget(scroll_view)

        close_button = Button(text="X", size_hint=(None, None), size=(25, 25), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=lambda instance: popup.dismiss())
        popup_content.add_widget(close_button)

        popup = Popup(title='Shop Entries', content=popup_content, size_hint=(None, None), size=popup_size)
        popup.open()

    def buy_stat(self, button, entry, price):
        if self.run.coins < price:
            return
        else:
            self.run.coins -= price

        match entry["name"]:
            case "1 Energy":
                self.run.energy += 1
                entry["times_bought"] += 1
                return
            case "1 HP":
                self.run.hp += 1
                entry["times_bought"] += 1
                return
            case "1 Skill Point":
                self.run.skill_points += 1
                entry["times_bought"] += 1
                return
        
        for tower in self.game_data.get_unlocked_towers():
            if tower == entry['name']:
                self.game_data.unlock_tower(entry['name'])
                entry['times_bought'] += 1
                return
        
        if entry["times_bought"] == entry["max_times_bought"]:
            button.text = "Maxed"
            button.disabled = True
            return

    def upgrade():
        pass