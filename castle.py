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
    def __init__(self, run, **kwargs):
        super().__init__(**kwargs)
        self.base_hp = 10
        self.base_energy = 2
        self.rect_size = (Window.width, 2)
        self.game_data = GameData()
        self.towers_in_use = {0: [None, None], 1: [None, None], 2: [None, None], 3: [None, None]}
        self.rect_pos = (0, Window.height * 0.2)
        self.run = run
        self.selected_button = None
        self.towers = None

        with self.canvas:
            Color(0, 1, 0, 1)  # Set the color to green
            self.rect = Rectangle(pos=self.rect_pos, size=self.rect_size)

        tower_position_size = (40, 40)
        tower_layout_size = (Window.width, tower_position_size[1])
        right_left_padding = 50
        self.tower_layout = BoxLayout(orientation='horizontal', 
                                    spacing=(Window.width - right_left_padding * 2 - tower_position_size[0] * 4) / 3, 
                                    size_hint=(None, None), 
                                    size=tower_layout_size, 
                                    pos=(0, Window.height * 0.2 - 2 - tower_layout_size[1]), 
                                    padding=[right_left_padding, 0]
                                    )

        for i in range(4):
            tower_position = Button(
                text='+', 
                size_hint=(None, None), 
                size=tower_position_size,
                background_normal='',
                background_color=(1, 0, 0, 1),
                background_disabled_normal='',
                )
            tower_position.bind(on_press=lambda btn, i=i: self.tower_selection(btn, i))
            self.tower_layout.add_widget(tower_position)
            #del self.towers_in_use[i] #Remove code later for better implementation
            selected_towers = self.game_data.get_selected_towers()
            for tower in selected_towers:
                if tower['position'] == i and tower['name'] != 'None':
                    Clock.schedule_once(lambda dt, t=tower['name'], i=i, tower_position=tower_position: self.set_current_tower(tower_position, t, i), 0.01)
                    break
                elif tower['position'] == i:
                    self.towers_in_use[i] = [tower_position, None]
                    break

    def set_current_tower(self, tower_position, tower_name, i):
        self.towers = self.run.tower_instances
        for tower in self.towers:
            if tower.name == tower_name:
                self.towers_in_use[i] = [tower_position, tower]
                tower.draw_to_screen(tower_position.pos)
                break
        self.tower_layout.add_widget(self.towers_in_use[i][1])
        
    def tower_selection(self, instance, position):
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols = 1, spacing = 10, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (300, 300)

        unlocked_towers = self.game_data.get_unlocked_towers()
        all_towers = self.run.tower_instances

        for full_tower in all_towers:
            for tower in unlocked_towers:
                if tower == full_tower.name:
                    button = Button(text=tower + " (lvl: " + str(full_tower.level) + ")", size_hint_y=None, height=40)
                    button.bind(on_press=lambda btn, t=tower: self.create_tower(btn, t, position=position))
                    grid_layout.add_widget(button)
                    
                if self.towers_in_use[position][1] is not None and self.towers_in_use[position][1].name == tower:
                    self.selected_button = button
                    button.background_color = (0, 1, 0, 1)
        
        popup_content.add_widget(grid_layout)  

        close_button = Button(text="Close", size_hint_y=None, height=50)
        close_button.bind(on_press=lambda *args: self.popup.dismiss())
        popup_content.add_widget(close_button)

        # Create the popup
        self.popup = Popup(title="Select a Tower", content=popup_content,
                           size_hint=(None, None), size=popup_size)

        # Open the popup
        self.popup.open()

    
    def create_tower(self, btn, tower_name, position):
        for tower in self.towers_in_use.values():
            if tower[1] is not None and tower[1].name == tower_name and tower[1] != self.towers_in_use[position][1]:
                return
        
        for tower in self.towers:
            if tower.name == tower_name:
                create_tower = tower
                break
        
        if self.towers_in_use[position][1] is not None and self.towers_in_use[position][1].name == tower_name:
            btn.background_color = (1, 1, 1, 1)
            self.tower_layout.remove_widget(self.towers_in_use[position][1])
            self.towers_in_use[position][1] = None
        else:
            if self.selected_button and self.selected_button != btn and self.towers_in_use[position][1] is not None:
                self.selected_button.background_color = (1, 1, 1, 1)
                self.tower_layout.remove_widget(self.towers_in_use[position][1])
            btn.background_color = (0, 1, 0, 1)
            self.towers_in_use[position][1] = create_tower
            self.selected_button = btn
            self.tower_layout.add_widget(create_tower)
                

        match tower_name:
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
        if self.rect_pos[1] >= enemy.pos[1]:
            self.run.hp -= enemy.damage
            self.parent.remove_widget(enemy)
            self.parent.round.enemies.remove(enemy)
            if enemy in self.parent.round.bullets_to_kill:
                del self.parent.round.bullets_to_kill[enemy]
            for bullet in self.parent.round.bullets:
                if bullet.enemy == enemy:
                    self.parent.round.bullets.remove(bullet)
                    self.parent.remove_widget(bullet)