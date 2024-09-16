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

class UpgradeWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        self.add_widget(layout)

        # Create a TabbedPanel
        tabbed_panel = TabbedPanel(do_default_tab=False)

        # Create tabs
        tab1 = TabbedPanelItem(text='Tab 1')
        layout1 = FloatLayout()
        tab2 = TabbedPanelItem(text='Tab 2')
        layout2 = FloatLayout()
        tab3 = TabbedPanelItem(text='Tab 3')
        layout3 = FloatLayout()

        # Example skills for each tab
        skills_tab1 = [
            {'name': 'Skill A1', 'pos': (0.4, 0.4), 'info': 'This is Skill A1'},
            {'name': 'Skill A2', 'pos': (0.6, 0.4), 'info': 'This is Skill A2'},
            {'name': 'Skill A3', 'pos': (0.4, 0.6), 'info': 'This is Skill A3'},
            {'name': 'Skill A4', 'pos': (0.6, 0.6), 'info': 'This is Skill A4'},
            {'name': 'Skill A5', 'pos': (0.5, 0.8), 'info': 'This is Skill A5'}
        ]
        skills_tab2 = [
            {'name': 'Skill B1', 'pos': (0.4, 0.4), 'info': 'This is Skill B1'},
            {'name': 'Skill B2', 'pos': (0.6, 0.4), 'info': 'This is Skill B2'},
            {'name': 'Skill B3', 'pos': (0.4, 0.6), 'info': 'This is Skill B3'},
            {'name': 'Skill B4', 'pos': (0.6, 0.6), 'info': 'This is Skill B4'},
            {'name': 'Skill B5', 'pos': (0.5, 0.8), 'info': 'This is Skill B5'}
        ]
        skills_tab3 = [
            {'name': 'Skill C1', 'pos': (0.4, 0.4), 'info': 'This is Skill C1'},
            {'name': 'Skill C2', 'pos': (0.6, 0.4), 'info': 'This is Skill C2'},
            {'name': 'Skill C3', 'pos': (0.4, 0.6), 'info': 'This is Skill C3'},
            {'name': 'Skill C4', 'pos': (0.6, 0.6), 'info': 'This is Skill C4'},
            {'name': 'Skill C5', 'pos': (0.5, 0.8), 'info': 'This is Skill C5'}
        ]

        # Function to create skill buttons and draw lines
        def create_skill_buttons_and_lines(skills, parent_layout, layout):
            skill_button_size = (50, 50)

            with layout.canvas:
                Color(1, 1, 1)
                Line(points=[Window.width * 0.4, Window.height * 0.4 + skill_button_size[0] / 2, Window.width * 0.4, Window.height * 0.6 - skill_button_size[1] / 2], width=2)
                Line(points=[Window.width * 0.6, Window.height * 0.4 + skill_button_size[0] / 2, Window.width * 0.6, Window.height * 0.6 - skill_button_size[1] / 2], width=2)
                Line(points=[Window.width * 0.4, Window.height * 0.6 + skill_button_size[0] / 2, Window.width * 0.5, Window.height * 0.8 - skill_button_size[1] / 2], width=2)
                Line(points=[Window.width * 0.6, Window.height * 0.6 + skill_button_size[0] / 2, Window.width * 0.5, Window.height * 0.8 - skill_button_size[1] / 2], width=2)

            for skill in skills:
                button = Button(text=skill['name'], size_hint=(None, None), size=skill_button_size)
                button.skill_info = skill['info']
                button.bind(on_press=self.show_skill_info_window)
                #button.pos_hint = {'center_x': skill['pos'][0], 'center_y': skill['pos'][1]}
                button.pos = (Window.width * skill['pos'][0] - skill_button_size[0] / 2, Window.height * skill['pos'][1] - skill_button_size[1] / 2)
                layout.add_widget(button)
            
            parent_layout.add_widget(layout)
        
        # Add skill buttons and lines to each tab
        create_skill_buttons_and_lines(skills_tab1, tab1, layout1)
        create_skill_buttons_and_lines(skills_tab2, tab2, layout2)
        create_skill_buttons_and_lines(skills_tab3, tab3, layout3)

        # Add tabs to the TabbedPanel
        tabbed_panel.add_widget(tab1)
        tabbed_panel.add_widget(tab2)
        tabbed_panel.add_widget(tab3)

        # Add the TabbedPanel to the layout
        layout.add_widget(tabbed_panel)
        

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