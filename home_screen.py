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

class HomeWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.perma_coins = 0
        buttons = []
        pass

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
        #start_run.bind(on_press=self.switch_to_play)
        button_layout.add_widget(start_run)
        buttons.append(start_run)

        perma_shop = Button(text="Perma Shop",
                             size_hint=(0.4, 1),
                            )
        perma_shop.bind(on_press=self.switch_to_perma_shop)
        button_layout.add_widget(perma_shop)
        buttons.append(perma_shop)

        self.add_widget(button_layout)

    def switch_to_play(self, instance):
        self.manager.current = 'Play'

    def switch_to_perma_shop(self, instance):
        self.manager.current = 'Shop'
    
    def on_enter(self):
        self.manager.get_screen('Shop').perma_coins = self.perma_coins
    
    def top_bar(self):
        layout = BoxLayout(orientation='horizontal', 
                           size=(Window.width, 30), 
                           pos=(0, Window.height - 30),
                           spacing=10,
                           padding=10
                           )
        
        perma_coins = Label(text="Perma Coins: " + str(self.perma_coins))
        layout.add_widget(perma_coins)
        self.add_widget(layout)

class PermanentShop(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.game_data = GameData()
        self.perma_coins = None
        self.shop_enteries(self)

    def shop_enteries(self, instance):
        layout = FloatLayout(pos=(0, 0), size=(Window.width, Window.height))
        grid_layout = GridLayout(cols = 2, spacing = 0, size_hint_y = None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        entries = self.game_data.get_shop_entries()
        for entry in entries:
            button1 = Button(text=entry['name'], size_hint_y=None, height=40)
            button2 = Button(text=str(entry['price']), size_hint_y=None, height=40)
            button2.bind(on_release=lambda btn, name=entry['name'], price=entry['price']: self.buy(name, price))
            grid_layout.add_widget(button1)
            grid_layout.add_widget(button2)
        layout.add_widget(grid_layout)
        self.add_widget(layout)
        #self.add_widget(popup_content)

    def buy(self, name, price):
        if self.perma_coins < price:
            return
        else:
            self.perma_coins -= price

        match name:
            case "Energy":
                self.run.energy += 1
                return
            case "1 HP":
                self.run.hp += 1
                return
            case "Skill Point":
                self.run.skill_points += 1
                return
        
        for tower in self.game_data.get_unlocked_towers():
            if tower['name'] == name:
                self.game_data.unlock_tower(name)
                return

    def upgrade():
        pass

    
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeWindow(name='Home'))
        sm.add_widget(PermanentShop(name='Shop'))
        return sm
        #return MyGame()

if __name__ == '__main__':
    MyApp().run()
