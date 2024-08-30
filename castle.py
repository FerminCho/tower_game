from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from game_data import GameData
import math

class Castle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hp = 10
        self.rect_size = (100, 100)
        self.game_data = GameData()

        self.rect_pos = (Window.width / 2 - self.rect_size[0] / 2, Window.height / 2 - self.rect_size[1] / 2 )

        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.rect_pos, size=self.rect_size)
        
        # Create a button
        self.tower_selection = Button(text='',
                        size=(20, 20),
                        pos=(self.rect.pos[0] + 10, self.rect.pos[1] + 10),
                        background_color = (1, 0, 0, 1),
                        background_normal = '')
        
        self.tower_selection.bind(on_press=self.towers)
        
        # Add button to the widget
        self.add_widget(self.tower_selection)
    
    def towers(self, instance):
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        towers = self.game_data.get_unlocked_towers()

        for tower in towers:
            button = Button(text=tower['name'], size_hint_y=None, height=40)
            button.bind(on_press=lambda btn, t=tower: self.create_tower(t))
            grid_layout.add_widget(button)
        
        popup_content.add_widget(grid_layout)

        close_button = Button(text="Close", size_hint_y=None, height=50)
        close_button.bind(on_press=lambda *args: self.popup.dismiss())
        popup_content.add_widget(close_button)

        # Create the popup
        self.popup = Popup(title="Select a Tower", content=popup_content,
                           size_hint=(None, None), size=(300, 300))

        # Open the popup
        self.popup.open()
    
    def create_tower(self, tower):
        tower_pos = self.tower_selection.pos
        match tower:
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