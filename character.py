import json
import random

with open('character_dictionary.json', 'r') as file:
    data = json.load(file)

class Character:
    def __init__(self):
        self.name = self.generate_name()
        self.profession_key, profession_data = self.choose_profession()
        self.profession = profession_data['profession_name']
        self.goal_description = profession_data['goal_description']
        self.goal_type = profession_data['goal_type']
        self.goal_value = profession_data['goal_value']
        self.description = random.choice(data['descriptions'])
        
      # List of attributes to be extracted with values and reasoning
        attributes = [
          'affectation_moisture', 'affectation_size', 'affectation_sound', 'affectation_light',
          'courage', 'attunement', 'knowledge', 'arcane', 'stealth', 'investigation'
      ]
      # Using a loop to assign values and reasoning to attributes
        for attr in attributes:
          value_key = f"{attr}_value"
          reasoning_key = f"{attr}_reasoning"
          setattr(self, value_key, profession_data[value_key])
          setattr(self, reasoning_key, profession_data[reasoning_key])

    

    def generate_name(self):
        """Generate a random name from the data."""
        first_name = random.choice(data['first_names'])
        last_name = random.choice(data['last_names'])
        return f"{first_name} {last_name}"

    def choose_profession(self):
        """Randomly choose a profession from the data."""
        profession_key = random.choice(list(data['professions'].keys()))
        return profession_key, data['professions'][profession_key]

    def display(self):
        """Return a formatted string of the character's details."""
        details = f"Name: {self.name}\nProfession: {self.profession}\nDescription: {self.description}\nGoal: {self.goal_description}\n"
        return details
      

