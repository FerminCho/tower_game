from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.energy_layout()

    def energy_layout(self):
        # Create the big layout using FloatLayout for absolute positioning
        layout_big = FloatLayout(
            size_hint=(None, None), 
            size=(Window.width, 40), 
            pos=(0, 200)
        )

        # Create the small layout
        layout_small = BoxLayout(
            orientation='vertical',
            spacing=5,
            size_hint=(None, None), 
            size=(40, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center the small layout within the big layout
        )

        # Add rectangles to the small layout
        with layout_small.canvas:
            for i in range(4):
                Color(1, 0, 0, 1)
                Rectangle(pos=(0, i * 10), size=(40, 2))  # Adjust the position of each rectangle
        
        # Add the small layout to the big layout
        layout_big.add_widget(layout_small)
        self.add_widget(layout_big)
        print(layout_small.pos)
        print(layout_big.pos)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlayWindow(name='Play'))
        sm.add_widget(UpgradeWindow(name='Upgrade'))
        return sm

class UpgradeWindow(Screen):
    pass

if __name__ == '__main__':
    MyApp().run()