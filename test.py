from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Color
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

Window.size = (800, 600)

class SkillTreeWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.add_widget(layout)

        # Define the skill tree layout
        skill_tree_layout = GridLayout(cols=3, rows=3, spacing=10, size_hint=(None, None))
        skill_tree_layout.bind(minimum_width=skill_tree_layout.setter('width'),
                               minimum_height=skill_tree_layout.setter('height'))
        skill_tree_layout.pos = (300, 300)
        layout.add_widget(skill_tree_layout)

        # Example skills
        skills = [
            {'name': 'Skill 1', 'pos': (0, 2), 'info': 'This is Skill 1'},
            {'name': 'Skill 2', 'pos': (1, 1), 'info': 'This is Skill 2'},
            {'name': 'Skill 3', 'pos': (2, 2), 'info': 'This is Skill 3'},
            {'name': 'Skill 4', 'pos': (1, 0), 'info': 'This is Skill 4'},
        ]

        # Create skill buttons
        for skill in skills:
            button = Button(text=skill['name'], size_hint=(None, None), size=(100, 100))
            button.skill_info = skill['info']
            button.bind(on_press=self.show_skill_info_window)
            skill_tree_layout.add_widget(button, index=skill['pos'][1] * 3 + skill['pos'][0])

        # Create a layout for the skill info window
        self.skill_info_window = BoxLayout(orientation='horizontal', size_hint=(0.5, None), height=100, pos_hint={'x': 0.25, 'y': 0})
        # Add a border to the BoxLayout
        with self.skill_info_window.canvas.before:
            Color(1, 0, 0, 1)  # Red color for the border
            self.border = Line(rectangle=(self.skill_info_window.x, self.skill_info_window.y, self.skill_info_window.width, self.skill_info_window.height), width=2)
        # Bind the size and position to update the border
        self.skill_info_window.bind(pos=self.update_border, size=self.update_border)

        self.skill_info_window.add_widget(Label(text='Skill Info', size_hint=(0.5, 1)))
        self.upgrade_button = Button(text='Upgrade', size_hint=(0.5, 1))
        self.skill_info_window.add_widget(self.upgrade_button)
        layout.add_widget(self.skill_info_window)
        self.skill_info_window.opacity = 0  # Initially hidden

        # Draw connections between skills
        with layout.canvas:
            Color(1, 1, 1)
            Line(points=[150, 300, 300, 200])  # Example line from Skill 1 to Skill 2
            Line(points=[300, 200, 450, 300])  # Example line from Skill 2 to Skill 3
            Line(points=[300, 200, 300, 100])  # Example line from Skill 2 to Skill 4

        # Add a button to go back to the PlayWindow
        back_button = Button(text="Back",
                             size_hint=(None, None),
                             size=(200, 100),
                             pos=(self.width / 2 - 100, 50))
        back_button.bind(on_press=self.switch_to_play)
        layout.add_widget(back_button)
    
    # Method to update the border
    def update_border(self, *args):
        self.border.rectangle = (self.skill_info_window.x, self.skill_info_window.y, self.skill_info_window.width, self.skill_info_window.height)

    def show_skill_info_window(self, instance):
        # Populate the skill info window with the relevant information
        self.skill_info_window.children[1].text = instance.skill_info
        self.skill_info_window.opacity = 1  # Show the skill info window

    def switch_to_play(self, instance):
        self.manager.current = 'Play'

class PlayWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.add_widget(layout)

        # Add a button to switch to the SkillTreeWindow
        skill_tree_button = Button(text="Skill Tree",
                                   size_hint=(None, None),
                                   size=(200, 100),
                                   pos=(self.width / 2 - 100, self.height / 2 - 50))
        skill_tree_button.bind(on_press=self.switch_to_skill_tree)
        layout.add_widget(skill_tree_button)

    def switch_to_skill_tree(self, instance):
        self.manager.current = 'SkillTree'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PlayWindow(name='Play'))
        sm.add_widget(SkillTreeWindow(name='SkillTree'))
        return sm

if __name__ == '__main__':
    MyApp().run()