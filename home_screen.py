from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Color
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from game_data import GameData
from kivy.properties import NumericProperty

class HomeWindow(Screen):
    perma_coins = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extra_coins = 0
        self.extra_skill_points = 0
        self.extra_energy = 0
        self.extra_hp = 0
        buttons = []
        self.game_data = GameData()

        button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width, 100), pos=(0, 0))

        library = Button(text="Library",
                         size_hint=(0.4, 1),
                         )
        #library.bind(on_press=self.switch_to_library)
        button_layout.add_widget(library)
        buttons.append(library)

        start_run = Button(text="New run",
                             size_hint=(0.3, 1),
                            )
        start_run.bind(on_press=self.switch_to_play)
        button_layout.add_widget(start_run)
        buttons.append(start_run)

        perma_shop = Button(text="Perma Shop",
                             size_hint=(0.4, 1),
                            )
        perma_shop.bind(on_press=self.switch_to_perma_shop)
        button_layout.add_widget(perma_shop)
        buttons.append(perma_shop)

        self.add_widget(button_layout)

        top_layout = BoxLayout(orientation='horizontal', 
                           size=(Window.width, 30), 
                           pos=(0, Window.height * 0.94),
                           spacing=10,
                           padding=10
                           )
        
        perma_coins_label = self.create_resource_label('Perma Coins: ', 'perma_coins', (0, 0), (1, 1, 1, 1))
        top_layout.add_widget(perma_coins_label)
        self.add_widget(top_layout)

    def switch_to_play(self, instance):
        self.manager.current = 'Play'

    def switch_to_perma_shop(self, instance):
        self.manager.current = 'Shop'

    def create_resource_label(self, prefix, property_name, pos, color):
        label = Label(text=prefix + str(getattr(self, property_name)),
                      size_hint=(None, None),
                      font_size=Window.width * 0.025,
                      pos=pos,
                      color=color)
        label.bind(texture_size=lambda instance, value: instance.setter('size')(instance, value))
        self.bind(**{property_name: lambda instance, value: label.setter('text')(label, prefix + str(value))})
        return label


class PermanentShop(Screen):
    perma_coins = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home = None
        self.game_data = GameData()
        self.shop_enteries(self)

    def shop_enteries(self, instance):
        self.layout = FloatLayout(pos=(0, 0), size=(Window.width, Window.height))
        grid_layout = GridLayout(cols = 2, spacing = 0, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        entries = self.game_data.get_permanent_shop_entries()
        for entry in entries:
            button1 = Button(text=entry['name'], size_hint_y=None, height=40)
            button2 = Button(text=str(entry['price']), size_hint_y=None, height=40)
            button2.bind(on_release=lambda btn, name=entry['name'], price=entry['price']: self.buy(name, price))
            grid_layout.add_widget(button1)
            grid_layout.add_widget(button2)
        self.layout.add_widget(grid_layout)
        
        back_button = Button(text='Back', size_hint=(None, None), size=(100, 50), pos=(10, 10))
        back_button.bind(on_release=self.go_back)
        self.layout.add_widget(back_button)

        self.perma_coins_label = Label(text=f'Perma Coins: {self.perma_coins}', 
                                       pos=(Window.width * 0.04, Window.height * 0.89), 
                                       size_hint=(None, None),
                                       font_size=Window.width * 0.025, 
                                       color=(1, 1, 1, 1))
        self.layout.add_widget(self.perma_coins_label)

        self.add_widget(self.layout)
    

    def on_enter(self):
        self.home = self.manager.get_screen('Home')
        self.perma_coins = self.home.perma_coins
        self.bind(perma_coins=self.update_home_perma_coins)
        self.home.bind(perma_coins=self.update_perma_coins)
        
    def update_home_perma_coins(self, instance, value):
        self.home.perma_coins = value

    def update_perma_coins(self, instance, value):
        self.perma_coins = value
        self.perma_coins_label.text = f'Perma Coins: {self.perma_coins}'
    
    def go_back(self, instance):
        self.manager.current = 'Home' 

    def buy(self, name, price):
        if self.perma_coins < price:
            return
        else:
            self.perma_coins -= price

        match name:
            case "+1 Permanent Energy":
                self.home.extra_energy += 1
                return
            case "+1 Permanent HP":
                self.home.extra_hp += 1
                return
            case "+1 Permanent skill point":
                self.home.extra_skill_point += 1
                return
        
        for tower in self.game_data.get_all_towers():
            if tower['name'] == name:
                self.game_data.unlock_tower(name)
                return
        
        self.save_buy()
        
    def save_buy(self):
        data = {'extra_energy': self.home.extra_energy, 
                'extra_hp': self.home.extra_hp, 
                'extra_skill_points': self.home.extra_skill_points,
                'exra_coins': self.home.extra_coins
                }

        self.game_data.save_perma_data(data)
        

    
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeWindow(name='Home'))
        sm.add_widget(PermanentShop(name='Shop'))
        return sm

if __name__ == '__main__':
    MyApp().run()

