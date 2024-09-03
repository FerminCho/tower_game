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
        self.rect_size = (100, 100)
        self.game_data = GameData()
        self.towers_in_use = {1 : None, 2 : None, 3 : None, 4 : None}

        self.rect_pos = (Window.width / 2 - self.rect_size[0] / 2, Window.height / 2 - self.rect_size[1] / 2 )

        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.rect_pos, size=self.rect_size)
        
        # Create a button
        self.tower_select_button = Button(text='',
                        size=self.rect_size,
                        pos=self.rect_pos,
                        background_normal = '',
                        opacity = 0)
        
        self.tower_select_button.bind(on_press=self.tower_selection)
        
        # Add button to the widget
        self.add_widget(self.tower_select_button)
    
    def tower_selection(self, instance):
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (300, 300)

        #towers = self.game_data.get_unlocked_towers()
        towers = [{'name': 'Tower 1'}, {'name': 'Tower 2'}, {'name': 'Tower 3'}]

        for tower in towers:
            button = Button(text=tower['name'], size_hint_y=None, height=40)
            button.bind(on_press=lambda btn, t=tower: self.create_tower(t))
            grid_layout.add_widget(button)
        
        popup_content.add_widget(grid_layout)

        # Create a BoxLayout at the bottom with horizontal alignment
        padding_x = 10
        num_buttons = 4
        button_width = 25
        spacing = (popup_size[0] - 25 * 4 - padding_x * 2) / 3
        bottom_layout_width = padding_x * 2 + button_width * num_buttons + spacing * (num_buttons - 1)
        bottom_layout = BoxLayout(orientation='horizontal', 
                                spacing=spacing, 
                                size_hint=(1, None), 
                                height = 50, 
                                padding=[padding_x, 10]
                                )

        for i in range(4):
            deselect_tower = Button(
                text='', 
                size_hint=(None, None), 
                size=(25, 25),
                background_normal='',
                background_color=(1, 0, 0, 1),
                background_disabled_normal='',
                disabled = True
                )
            #deselect_tower.bind(disabled = True)
            bottom_layout.add_widget(deselect_tower)

        popup_content.add_widget(bottom_layout)  

        close_button = Button(text="Close", size_hint_y=None, height=50)
        close_button.bind(on_press=lambda *args: self.popup.dismiss())
        popup_content.add_widget(close_button)

        # Create the popup
        self.popup = Popup(title="Select a Tower", content=popup_content,
                           size_hint=(None, None), size=popup_size)

        # Open the popup
        self.popup.open()
    
    def create_tower(self, tower_info):
        create_tower = Tower(fire_rate=1, damage=1, level=1)
        self.towers_in_use.append(create_tower)
        self.add_widget(create_tower)

        empty = 0
        for key, value in self.towers_in_use:
            if value == None:
                self.towers_in_use[key] = create_tower
                break
            else:
                empty += 1
            if empty == 4:
                print("full")

        match tower_info:
            case 0:
                return
            case 1:
                return
    
    def detect_collision(self, enemy):
        castle_center = (
            self.pos[0] + self.rect_size[0] / 2,
            self.pos[1] + self.rect_size[1] / 2
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