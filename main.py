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
from round import Round, run, shop
import random
import math

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.layout = FloatLayout(size=(Window.width, Window.height))
        self.main_buttons = []
        self.castle = Castle()
        self.run = run(castle=self.castle)
        self.shop = shop(run=self.run, castle=self.castle)
        self.add_widget(self.castle)
        self.add_widget(self.castle.tower_layout)
        self.energy_layout()
        self.resource_layout()


        run_buttons = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width, 100), pos=(0, 0))

        # Add a button to switch to the UpgradeWindow
        upgrade_button = Button(text="Upgrade Tower",
                                size_hint=(0.3, 1),
                                size=(200, 100),
                                pos=(0, 0))
        upgrade_button.bind(on_press=self.switch_to_upgrade)
        self.main_buttons.append([upgrade_button, upgrade_button.size_hint[0]])
        run_buttons.add_widget(upgrade_button)

        self.start_button = Button(text="Start Round",
                                   size_hint=(0.4, 1),
                                   #size=self.start_button_size,
                                   #pos=(Window.width / 2 - self.start_button_size[0] / 2, 0)
                                   )
        self.start_button.bind(on_press=self.start_game)
        self.main_buttons.append([self.start_button, self.start_button.size_hint[0]])
        run_buttons.add_widget(self.start_button)
         
        self.shop_button = Button(text="Shop",
                            size_hint=(0.3, 1),
                            #size=(200, 100),
                            )
        self.shop_button.bind(on_press=self.shop.shop_enteries)
        self.main_buttons.append([self.shop_button, self.shop_button.size_hint[0]])
        run_buttons.add_widget(self.shop_button)

        self.add_widget(run_buttons)
        self.round = Round(main_buttons=self.main_buttons, castle=self.castle, layout=self, run=self.run)

    def switch_to_upgrade(self, instance):
        self.manager.current = 'Upgrade'

    def start_game(self, instance):   
        Clock.schedule_once(self.round.start, 0.01)

    def energy_layout(self):
        self.energy_buttons = []
        button_size = (40, 40)
        self.energy_state = 'add'
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
                                        background_disabled_normal='',
                                        energy_state=self.energy_state,
                                        run=self.run
                                        )
            self.energy_buttons.append(self.energy_button)
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
        toggle_button.bind(on_press=self.on_toggle)
        self.add_widget(toggle_button)
    
    def on_toggle(self, instance):
        if instance.state == 'down':
            for button in self.energy_buttons:
                button.energy_state = 'remove'
            instance.text = 'Energy -'
        else:
            for button in self.energy_buttons:
                button.energy_state = 'add'
            instance.text = 'Energy +'
    
    def resource_layout(self):
        resources = ResourceHandling()
        layout = BoxLayout(orientation='horizontal', 
                           size=(Window.width, 30), 
                           pos=(0, Window.height - 30),
                           spacing=10,
                           padding=10
                           )
        
        energy_label = self.create_resource_label('Energy: ', 'energy', (0, Window.height - 30), (1, 1, 1, 1))
        layout.add_widget(energy_label)
        
        coins_label = self.create_resource_label('Coins: ', 'coins', (energy_label.width, Window.height - 30), (1, 1, 1, 1))
        layout.add_widget(coins_label)

        round_label = self.create_resource_label('Round: ', 'round', (energy_label.width, Window.height - 30), (1, 1, 1, 1))
        layout.add_widget(round_label)

        skill_points_label = self.create_resource_label('Skill Points: ', 'skill_points', (energy_label.width, Window.height - 30), (1, 1, 1, 1))
        layout.add_widget(skill_points_label)
        
        self.add_widget(layout)

    def create_resource_label(self, prefix, property_name, pos, color):
        label = Label(text=prefix + str(getattr(self.run, property_name)),
                      size_hint=(None, None),
                      font_size=Window.width * 0.025,
                      pos=pos,
                      color=color)
        label.bind(texture_size=lambda instance, value: instance.setter('size')(instance, value))
        self.run.bind(**{property_name: lambda instance, value: label.setter('text')(label, prefix + str(value))})
        return label

class BorderButton(Button):
    def __init__(self, energy_state, run, **kwargs):
        super(BorderButton, self).__init__(**kwargs)
        self.energy_state = energy_state
        self.run = run
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
                    self.run.energy -= 1
                    break
        else:
            for color, rect in self.rectangles:
                if color.rgba == [1, 1, 1, 1]:  # Check if the color is white
                    color.rgba = (1, 0, 0, 1)  # Change the color to red
                    self.run.energy += 1
                    break
    
    def set_energy_state(self, new_state):
        self.energy_state = new_state
     
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlayWindow(name = 'Play'))
        sm.add_widget(UpgradeWindow(name = 'Upgrade'))
        return sm
        #return MyGame()

if __name__ == '__main__':
    MyApp().run()