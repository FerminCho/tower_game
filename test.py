from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

class BorderButton(Button):
    def __init__(self, **kwargs):
        super(BorderButton, self).__init__(**kwargs)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Border color
            Line(rectangle=(self.x, self.y, self.width, self.height), width=2)  # Border width

    def update_rectangles(self, instance, value):
        for j, (color_instruction, rect) in enumerate(self.rectangles):
            rect.pos = (instance.pos[0], j * 10 + instance.pos[1] + 2)
    
    def remove_energy(self, instance):
        for color_instruction, rect in self.rectangles:
            if color_instruction.rgba == [1, 0, 0, 1]:  # Check if the color is red
                print('Removing energy')
                color_instruction.rgba = (0, 1, 0, 1)  # Change the color to green
                break

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.energy_layout()

    def energy_layout(self):
        # Create the big layout using BoxLayout for relative positioning
        layout_big = BoxLayout(
            orientation='horizontal',
            spacing=0.05,  # Relative spacing
            size_hint=(1, None), 
            height=0.1 * Window.height,  # Relative height
            pos_hint={'center_x': 0.5, 'center_y': 0.2}  # Relative position
        )

        for i in range(4):
            energy_button = BorderButton(
                text='+', 
                size_hint=(None, None), 
                size=(0.1 * Window.width, 0.1 * Window.width),  # Relative size
                background_normal='',
                background_color=(0, 1, 0, 1),
                background_disabled_normal=''
            )
            
            with energy_button.canvas:
                energy_button.rectangles = []
                for j in range(4):
                    color_instruction = Color(1, 0, 0, 1)
                    energy_rect = Rectangle(size=(energy_button.width, energy_button.height / 20))
                    energy_button.rectangles.append((color_instruction, energy_rect))
            energy_button.bind(pos=energy_button.update_rectangles, size=energy_button.update_rectangles)
            energy_button.bind(on_press=energy_button.remove_energy)  # Bind button press to remove_energy
            layout_big.add_widget(energy_button)
        
        self.add_widget(layout_big)

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