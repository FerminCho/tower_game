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
from round import Round, run
import random
import math

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.layout = FloatLayout(size=(Window.width, Window.height))
        self.main_buttons = []
        self.castle = Castle()
        self.run = run()
        self.add_widget(self.castle)
        self.add_widget(self.castle.tower_layout)
        self.energy_layout()
        self.resource_layout()

        # Create the start button
        self.start_button_size = (200, 100)
        self.start_button = Button(text="Start Round",
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
                                        energy_state=self.energy_state
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
            text='Coins: ' + str(self.run.coins),
            size_hint=(None, None),
            font_size=Window.width * 0.025,
            pos=(energy_label.width, Window.height - 30),
            color=(1, 1, 1, 1),
        )
        coins_label.bind(texture_size=lambda instance, value: instance.setter('size')(instance, value))
        self.run.bind(coins=lambda instance, value: coins_label.setter('text')(coins_label, 'Coins: ' + str(value)))
        layout.add_widget(coins_label)

        round_label = Label(
            text='Round: ' + str(self.run.round),
            size_hint=(None, None),
            font_size=Window.width * 0.025,
            pos=(energy_label.width, Window.height - 30),
            color=(1, 1, 1, 1),
        )
        round_label.bind(texture_size=lambda instance, value: instance.setter('size')(instance, value))
        layout.add_widget(round_label)
        
        self.add_widget(layout)

    def update_coins_label(self):
        self.coins_label.text = 'Coins: ' + str(self.run.coins)

class BorderButton(Button):
    def __init__(self, energy_state, **kwargs):
        super(BorderButton, self).__init__(**kwargs)
        self.energy_state = energy_state
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
        print(self.energy_state)
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