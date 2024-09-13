from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from game_data import GameData
from tower import Tower
import math

class Castle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hp = 10
        self.rect_size = (Window.width, 2)
        self.game_data = GameData()
        self.towers_in_use = {0: [None, None], 1: [None, None], 2: [None, None], 3: [None, None]}
        self.rect_pos = (0, Window.height * 0.2)
        self.selected_button = None

        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.rect_pos, size=self.rect_size)
        
        self.tower_button_size = (200, 100)
        # Create a button
        self.tower_select_button = Button(text='Select Tower',
                        size=self.tower_button_size,
                        pos=(Window.width - self.tower_button_size[0], 0),
                        background_normal = '',
                        background_color=(0, 1, 0, 1)
                        )
        
        self.tower_select_button.bind(on_press=self.tower_selection)
        
        # Add button to the widget
        self.add_widget(self.tower_select_button)

        tower_layout_size = (Window.width, 25)
        self.tower_layout = BoxLayout(orientation='horizontal', 
                                    spacing=10, 
                                    size_hint=(None, None), 
                                    size=(Window.width, 25), 
                                    pos=(0, Window.height * 0.2 - 2 - tower_layout_size[1]), 
                                    padding=[10, 0]
                                    )

        for i in range(4):
            tower_position = Button(
                text='+', 
                size_hint=(None, None), 
                size=(25, 25),
                background_normal='',
                background_color=(1, 0, 0, 1),
                background_disabled_normal='',
                )
            tower_position.bind(on_press=lambda btn, i=i: self.tower_selection(btn, i))
            self.tower_layout.add_widget(tower_position)
            del self.towers_in_use[i] #Remove code later for better implementation
            selected_towers = self.game_data.get_selected_towers()
            for tower in selected_towers:
                if tower['position'] == i and tower['name'] != 'None':
                    self.towers_in_use[i] = [tower_position, Tower(fire_rate=tower['fire_rate'], 
                                                                   damage=tower['damage'], 
                                                                   level=tower['level'], 
                                                                   name=tower['name'], 
                                                                   bullet_size=tower['size'], 
                                                                   tower_pos=tower_position.pos,
                                                                   castle_pos=self.rect_pos)]
                    break
                elif tower['position'] == i:
                    self.towers_in_use[i] = [tower_position, None]
                    break     
    
    def tower_selection(self, instance, position):
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (300, 300)

        towers = self.game_data.get_unlocked_towers()

        for tower in towers:
            button = Button(text=tower['name'], size_hint_y=None, height=40)
            button.bind(on_press=lambda btn, t=tower: self.create_tower(btn, t, position=position))
            grid_layout.add_widget(button)
            if self.towers_in_use[position][1] != None and self.towers_in_use[position][1].name == tower['name']:
                button.color = (1, 0, 0, 1)
                self.selected_button = button
        
        popup_content.add_widget(grid_layout)  

        close_button = Button(text="Close", size_hint_y=None, height=50)
        close_button.bind(on_press=lambda *args: self.popup.dismiss())
        popup_content.add_widget(close_button)

        # Create the popup
        self.popup = Popup(title="Select a Tower", content=popup_content,
                           size_hint=(None, None), size=popup_size)

        # Open the popup
        self.popup.open()
    
    def disable_button(self, instance):
        if not instance.disabled:
            instance.disabled = True
            instance.background_color = (1, 0, 0, 1)
            for key, value in self.towers_in_use.items():
                if value == self.towers_in_use[instance]:
                    self.towers_in_use[key] = None
                    return

    
    def create_tower(self, instance, tower_info, position):
        create_tower = Tower(fire_rate=tower_info['fire_rate'], 
                             damage=tower_info['damage'], 
                             level=tower_info['level'], 
                             name=tower_info['name'], 
                             bullet_size=tower_info['size'], 
                             tower_pos=self.towers_in_use[position][0].pos,
                             castle_pos=self.rect_pos
                            )
        
        if self.towers_in_use[position][1] != None and self.towers_in_use[position][1].name == tower_info['name']:
            instance.color = (1, 1, 1, 1)
            self.tower_layout.remove_widget(self.towers_in_use[position][1])
            self.towers_in_use[position][1] = None
        else:
            self.towers_in_use[position][1] == create_tower
            instance.color = (1, 0, 0, 1)
            self.selected_button.color = (1, 1, 1, 1)
            self.selected_button = instance
            self.tower_layout.add_widget(create_tower)

        match tower_info:
            case 0:
                return
            case 1:
                return
    
    def detect_collision(self, enemy):
        castle_center = (
            self.rect_pos[0] + self.rect_size[0] / 2,
            self.rect_pos[1] + self.rect_size[1] / 2
        )
        enemy_center = (
            enemy.pos[0] + enemy.rect_size[0] / 2,
            enemy.pos[1] + enemy.rect_size[1] / 2
        )

        # Calculate the distance between the tower and enemy
        distance = math.sqrt(
            (castle_center[0] - enemy_center[0]) ** 2 +
            (castle_center[1] - enemy_center[1]) ** 2
        )

        # Check if the distance is less than the sum of the radii (or half the widths)
        if distance < (self.rect_size[0] / 2 + enemy.rect_size[0] / 2):
            self.hp -= enemy.damage
            self.parent.remove_widget(enemy)
            self.parent.enemies.remove(enemy)
            self.parent.bullets_to_kill.pop(enemy)
            for bullet in self.parent.bullets:
                if bullet.enemy == enemy:
                    self.parent.bullets.remove(bullet)
                    self.parent.remove_widget(bullet)