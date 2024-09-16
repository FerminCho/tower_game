from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Ellipse, Color
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout

class CircleButton(RelativeLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.button = Button(text=text, size_hint=(1, 1))
        self.add_widget(self.button)
        with self.canvas:
            self.circle_color = Color(1, 0, 0, 1)  # Red color for the circle
            self.circle = Ellipse(size=(20, 20))
        self.button.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = (self.button.x + self.button.width - 25, self.button.y + 10)
        self.circle.size = (20, 20)

    def change_circle_color(self, color):
        self.circle_color.rgba = color

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_button = Button(text='Start')
        self.add_widget(self.start_button)
        self.towers_in_use = {0: [None, None]}  # Example data
        self.game_data = self  # Example data
        self.enemies = []
        self.bullets = []
        self.bullets_to_kill = {}

    def get_unlocked_towers(self):
        return [{'name': 'Tower 1'}, {'name': 'Tower 2'}]  # Example data

    def tower_selection(self, instance, position):
        # Create content for the popup
        popup_content = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        popup_size = (300, 300)

        towers = self.get_unlocked_towers()

        for tower in towers:
            button = CircleButton(text=tower['name'], size_hint_y=None, height=40)
            button.button.bind(on_press=lambda btn, t=tower: self.create_tower(btn, t, position=position))
            grid_layout.add_widget(button)
            print(f"Added button for tower: {tower['name']}")

            if self.towers_in_use[position][1] is not None and self.towers_in_use[position][1].name == tower['name']:
                button.change_circle_color((0, 1, 0, 1))  # Change to green color
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
        print("Popup opened")

    def create_tower(self, btn, tower_info, position):
        btn.change_circle_color((0, 1, 0, 1))
        print(f"Creating tower: {tower_info['name']} at position {position}")

class TowerSelectionApp(App):
    def build(self):
        game = Game()
        game.tower_selection(None, 0)
        return game

if __name__ == '__main__':
    TowerSelectionApp().run()