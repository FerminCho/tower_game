from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from enemies import Enemy

Window.size = (800, 600)

class MyGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.enemy = Enemy()
        self.add_widget(self.enemy)
        
class MyApp(App):
    def build(self):
        return MyGame()

if __name__ == '__main__':
    MyApp().run()