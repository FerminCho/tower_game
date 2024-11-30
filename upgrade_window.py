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

class UpgradeWindow(Screen):
    def __init__(self, play_window, run, **kwargs):
        super().__init__(**kwargs)
        self.play_window = play_window
        self.unlocked_towers = None
        self.run = run
        self.game_data = GameData()
        self.towers = self.game_data.get_all_towers()
        self.skill_buttons = []
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

        skill_point_label1 = self.play_window.create_resource_label('Skill Points: ', 'skill_points', (10, Window.height * 0.90), (1, 1, 1, 1))
        layout1.add_widget(skill_point_label1)
        skill_point_label2 = self.play_window.create_resource_label('Skill Points: ', 'skill_points', (10, Window.height * 0.90), (1, 1, 1, 1))
        layout2.add_widget(skill_point_label2)

        # Example skills for each tab
        self.skills_tab1 = [
            {'name': 'Skill A1', 'pos': (0.4, 0.4), 'info': 'This is Skill A1', "Upgraded": False},
            {'name': 'Skill A2', 'pos': (0.6, 0.4), 'info': 'This is Skill A2', "Upgraded": False},
            {'name': 'Skill A3', 'pos': (0.4, 0.6), 'info': 'This is Skill A3', "Upgraded": False},
            {'name': 'Skill A4', 'pos': (0.6, 0.6), 'info': 'This is Skill A4', "Upgraded": False},
            {'name': 'Skill A5', 'pos': (0.5, 0.8), 'info': 'This is Skill A5', "Upgraded": False},
            "Basic Tower",
        ]
        self.skills_tab2 = [
            {'name': 'Skill B1', 'pos': (0.4, 0.4), 'info': 'This is Skill B1', "Upgraded": False},
            {'name': 'Skill B2', 'pos': (0.6, 0.4), 'info': 'This is Skill B2', "Upgraded": False},
            {'name': 'Skill B3', 'pos': (0.4, 0.6), 'info': 'This is Skill B3', "Upgraded": False},
            {'name': 'Skill B4', 'pos': (0.6, 0.6), 'info': 'This is Skill B4', "Upgraded": False},
            {'name': 'Skill B5', 'pos': (0.5, 0.8), 'info': 'This is Skill B5', "Upgraded": False},
            "Sniper Tower",
        ]
        skills_tab3 = [
            {'name': 'Skill C1', 'pos': (0.4, 0.4), 'info': 'This is Skill C1', "Upgraded": False},
            {'name': 'Skill C2', 'pos': (0.6, 0.4), 'info': 'This is Skill C2', "Upgraded": False},
            {'name': 'Skill C3', 'pos': (0.4, 0.6), 'info': 'This is Skill C3', "Upgraded": False},
            {'name': 'Skill C4', 'pos': (0.6, 0.6), 'info': 'This is Skill C4', "Upgraded": False},
            {'name': 'Skill C5', 'pos': (0.5, 0.8), 'info': 'This is Skill C5', "Upgraded": False},
            "Cannon Tower",
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

            for skill in skills[:-1]:
                button = Button(text=skill['name'], size_hint=(None, None), size=skill_button_size)
                button.skill_info = skill['info']
                button.bind(on_press=lambda instance, tower_name=skills[-1], skill=skill: self.show_skill_info_window(instance, tower_name, skill))
                #button.pos_hint = {'center_x': skill['pos'][0], 'center_y': skill['pos'][1]}
                button.pos = (Window.width * skill['pos'][0] - skill_button_size[0] / 2, Window.height * skill['pos'][1] - skill_button_size[1] / 2)
                layout.add_widget(button)
                self.skill_buttons.append(button)
            
            parent_layout.add_widget(layout)
        
        # Add skill buttons and lines to each tab
        create_skill_buttons_and_lines(self.skills_tab1, tab1, layout1)
        create_skill_buttons_and_lines(self.skills_tab2, tab2, layout2)
        create_skill_buttons_and_lines(skills_tab3, tab3, layout3)
        self.show_sniper_selection_window(layout3)

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

        self.skill_info_window.add_widget(Label(text='', size_hint=(0.5, 1)))
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

    def show_skill_info_window(self, instance, tower_name, skill):
        for tower in self.run.tower_instances:
            if tower.name == tower_name:
                break
        # Populate the skill info window with the relevant information
        self.upgrade_button.bind(on_press=lambda button, tower=tower, skill=skill: self.upgrade(button, tower, skill))
        self.skill_info_window.children[1].text = instance.skill_info
        self.skill_info_window.opacity = 1  # Show the skill info window

        if skill['Upgraded']:
            self.upgrade_button.text = 'Upgraded'
            self.upgrade_button.disabled = True
        else:
            self.upgrade_button.text = 'Upgrade'
            self.upgrade_button.disabled = False
    
    def show_sniper_selection_window(self, layout):
        self.sniper_selection_window = BoxLayout(orientation='horizontal', spacing=(20), size_hint=(1.0, None), height=50, pos_hint={'x': 0, 'y': 0.91}, padding=10)
        self.basic_enemy_button = Button(text='Basic\nEnemy', size_hint=(None, None), size=(60, 50))
        self.basic_enemy_button.bind(on_press=lambda button: self.change_color(button, 'Basic Enemy'))
        self.fast_enemy_button = Button(text='Fast\nEnemy', size_hint=(None, None), size=(60, 50))
        self.fast_enemy_button.bind(on_press=lambda button: self.change_color(button, 'Fast Enemy'))
        self.armor_enemy_button = Button(text='Fast\nEnemy', size_hint=(None, None), size=(60, 50))
        self.armor_enemy_button.bind(on_press=lambda button: self.change_color(button, 'Fast Enemy'))
    
        self.sniper_selection_window.add_widget(self.basic_enemy_button)
        self.sniper_selection_window.add_widget(self.fast_enemy_button)
        self.sniper_selection_window.add_widget(self.armor_enemy_button)
        
    
        layout.add_widget(self.sniper_selection_window)
    
    def change_color(self, button, enemy_name):
        if button.color == (1, 0, 0, 1):
            button.color = (1, 1, 1, 1)
        if enemy_name == 'Basic Enemy':
            self.basic_enemy_button.color = (1, 0, 0, 1)
            self.fast_enemy_button.color = (1, 1, 1, 1)
        elif enemy_name == 'Fast Enemy':
            self.basic_enemy_button.color = (1, 1, 1, 1)
            self.fast_enemy_button.color = (1, 0, 0, 1)
    
    def upgrade(self, button, tower, skill):
        if self.run.skill_points == 0:
            return

        if tower.name == "Basic Tower":
            match skill['name']:
                case "Skill A1":
                    tower.base_damage += 1
                    self.run.skill_points -= 1
                    skill['Upgraded'] = True
                    self.upgrade_button.text = 'Upgraded'
                    self.upgrade_button.disabled = True
                    for skill_button in self.skill_buttons:
                        if skill_button.text == "Skill A1":
                            skill_button.color = (1, 0, 0, 1)
                case "Skill A2":
                    tower.fire_rate += 1
                    self.run.skill_points -= 1
                case "Skill A3":
                    tower.damage += 1
                    self.run.skill_points -= 1
                case "Skill A4":
                    tower.fire_rate += 1
                    self.run.skill_points -= 1
                case "Skill A5":
                    if self.run.skill_points <= 2:
                        return
                    tower.damage += 1
                    self.run.skill_points -= 2

        elif tower.name == "Sniper Tower":
            pass

        elif tower.name == "Burst Tower":
            match skill['name']:
                case "Skill C1":
                    tower.extra_burst_bullets += 1
                    self.run.skill_points -= 1
                case "Skill C2":
                    tower.tower_damage += 1
                    self.run.skill_points -= 1
                case "Skill C3":
                    tower.extra_burst_bullets += 1
                    self.run.skill_points -= 1
                case "Skill C4":
                    tower.tower_damage += 1
                    self.run.skill_points -= 1
                case "Skill C5":
                    if self.run.skill_points <= 2:
                        return
                    tower.ultimate_unlocked = True
                    self.run.skill_points -= 2
    
    def reset_upgrades(self):
        for skill_button in self.skill_buttons:
            skill_button.color = (1, 1, 1, 1)
        
        for skill in self.skills_tab1[:-1]:
            skill['Upgraded'] = False
        for skill in self.skills_tab2[:-1]:
            skill['Upgraded'] = False
        
        self.skill_info_window.opacity = 0

    def switch_to_play(self, instance):
        self.manager.current = 'Play'