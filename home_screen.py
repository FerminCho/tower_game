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
        layout = FloatLayout()
        self._disabled_count = 0
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
        start_run.bind(on_press=self.switch_to_play)
        button_layout.add_widget(start_run)
        buttons.append(start_run)

        perma_shop = Button(text="Perma Shop",
                             size_hint=(0.4, 1),
                            )
        #perma_shop.bind(on_press=self.switch_to_shop)
        button_layout.add_widget(perma_shop)
        buttons.append(perma_shop)

        #layout.add_widget(button_layout)
        self.add_widget(button_layout)

    def switch_to_play(self, instance):
        self.manager.current = 'Play'
    
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeWindow(name='Home'))
        return sm
        #return MyGame()

if __name__ == '__main__':
    MyApp().run()

