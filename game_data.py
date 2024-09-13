import json

class GameData():
    def __init__(self, file_name='game_data.json'):
        self.file_name = file_name
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_name, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"unlocked_towers": []}

    def save_data(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file)

    def unlock_tower(self, tower_name):
        if tower_name not in self.data['unlocked_towers']:
            self.data['unlocked_towers'].append(tower_name)
            self.save_data()

    def get_unlocked_towers(self):
        return self.data['unlocked_towers']
    
    def get_selected_towers(self):
        return self.data['selected_towers']