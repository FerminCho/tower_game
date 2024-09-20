from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

class GameData:
    def get_shop_entries(self):
        # Mock data for testing
        return [
            {'name': 'Item 1', 'price': 10},
            {'name': 'Item 2', 'price': 20},
            {'name': 'Item 3', 'price': 30},
            {'name': 'Item 4', 'price': 40},
        ]

class shop:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_data = GameData()
    
    def shop_entries(self):
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols=2, spacing=0, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (Window.width * 0.8, Window.height * 0.8)

        entries = self.game_data.get_shop_entries()
        for entry in entries:
            button1 = Button(text=entry['name'], size_hint_y=None, height=40, size_hint_x=0.8)
            button2 = Button(text=str(entry['price']), size_hint_y=None, height=40, size_hint_x=0.2)
            button2.bind(on_release=lambda btn, name=entry['name'], price=entry['price']: self.buy(name, price))
            grid_layout.add_widget(button1)
            grid_layout.add_widget(button2)
        popup_content.add_widget(grid_layout)
        popup = Popup(title='Shop Entries', content=popup_content, size_hint=(None, None), size=popup_size)
        popup.open()

    def buy(self, name, price):
        if self.castle.coins < int(price):
            return
        else:
            self.castle.coins -= int(price)
        match name:
            case "Energy":
                self.castle.energy += 1
            case "HP":
                self.castle.hp += 1

    def upgrade(self):
        pass

class ShopApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        shop_instance = shop()

        open_shop_button = Button(text='Open Shop', size_hint=(None, None), size=(200, 50))
        open_shop_button.bind(on_release=lambda x: shop_instance.shop_entries())

        main_layout.add_widget(open_shop_button)
        return main_layout

if __name__ == '__main__':
    ShopApp().run()