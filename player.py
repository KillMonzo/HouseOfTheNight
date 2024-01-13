from character import Character
from location import Location

class Player:

    def __init__(self, character: Character):
        self.name = character.name
        self.profession = character.profession
        self.description = character.description
        self.goal = character.goal_description
        self.affectation_moisture_value = character.affectation_moisture_value
        self.affectation_size_value = character.affectation_size_value
        self.affectation_light_value = character.affectation_light_value
        self.affectation_sound_value = character.affectation_sound_value
        self.courage_value = character.courage_value
        self.attunement_value = character.attunement_value
        self.knowledge_value = character.knowledge_value 
        self.arcane_value = character.arcane_value
        self.stealth_value = character.stealth_value
        self.investigation_value = character.investigation_value
        self.affectation_moisture_reasoning = character.affectation_moisture_reasoning
        self.affectation_size_reasoning = character.affectation_size_reasoning
        self.affectation_light_reasoning = character.affectation_light_reasoning
        self.affectation_sound_reasoning = character.affectation_sound_reasoning
        self.courage_reasoning = character.courage_reasoning
        self.attunement_reasoning = character.attunement_reasoning
        self.knowledge_reasoning = character.knowledge_reasoning
        self.arcane_reasoning = character.arcane_reasoning
        self.stealth_reasoning = character.stealth_reasoning
        self.investigation_reasoning = character.investigation_reasoning

        self.modifiers = {
            'courage': 0,
            'attunement': 0,
            'knowledge': 0,
            'arcane': 0,
            'stealth': 0,
            'investigation': 0,
            'actions': 0,
            'skillroll': 0,
        }
        self.equipment = []
        self.consumables = []
        self.items = self.equipment + self.consumables
        self.current_location = None
        self.max_actions = 3
        self.remaining_actions = self.max_actions
        self.cleared_locations = []
        self.equipment_storage = 2
        self.consumables_storage = 2
        self.experience = 0
        self.level = 1
        self.keys = 1
        
        self.fear = 0
        self.goal_item = None
        self.goal_type = character.goal_type
        self.goal_value = character.goal_value
        self.goal_met = False
        self.cleared_location_count = 0
        self.attempted_encounter_count = 0
        self.cleared_encounter_count = 0
        self.cleared_courage_count = 0
        self.cleared_attunement_count = 0
        self.cleared_knowledge_count = 0
        self.cleared_arcane_count = 0
        self.cleared_stealth_count = 0
        self.cleared_investigation_count = 0
        self.rooms_visited = 0

        self.common_count = 0
        self.uncommon_count = 0
        self.rare_count = 0
        self.ultrarare_count = 0

        self.starting_item = None

    def has_achieved_goal(self,game):
      goal_type = self.goal_type
      goal_value = self.goal_value
      # Add conditions based on the goal type
      if goal_type == 'investigation_clears':
          return self.cleared_investigation_count >= goal_value
      elif goal_type == 'courage_clears':
          return self.cleared_courage_count >= goal_value
      elif goal_type == 'attunement_clears':
          return self.cleared_attunement_count >= goal_value
      elif goal_type == 'knowledge_clears':
          return self.cleared_knowledge_count >= goal_value
      elif goal_type == 'arcane_clears':
          return self.cleared_arcane_count >= goal_value
      elif goal_type == 'stealth_clears':
          return self.cleared_stealth_count >= goal_value
      elif goal_type == 'encounter_clears':
          return self.cleared_encounter_count >= goal_value
      elif goal_type == 'location_clears':
          return self.cleared_location_count >= goal_value
      elif goal_type == 'rooms_unlocked':
          return self.rooms_visited >= game.total_locations
      elif goal_type == 'attempted_encounter_count':
          return self.attempted_encounter_count >= goal_value
      elif goal_type == 'item_clears':
          return self.common_count >= goal_value and self.uncommon_count >= goal_value and self.rare_count >= goal_value and self.ultrarare_count >= goal_value
      # ... other goal type conditions
        
    def unlock_foyer(self,game):
        
      print("Name: The Foyer")
      print("Description: A room suddenly appears in front of you. It is a large room with a large door at the end.")
      print("Ambiance: A bright light shines through the room, casting a warm glow on the walls, and the air is filled with a sense of tranquility.")
      print("Affectations:")
      print("Sound: 99 - The sounds echo into forever, creating the most beautiful harmonies.")
      print("Moisture: 99 - The air is dewy and fresh, like the spring of life.")
      print("Light: 99 - The sun has broken through the deep mist and cast down The Moon")
      print("Size: 99 - Infinitely stretching, it grows even now.")

      
          # Unlock the foyer logic here
          # For instance, set a boolean flag or modify a game state to unlock 'The Foyer'
  
    def check_for_goal(self,game):
        if self.has_achieved_goal(game):
            print("\n" + "*-"*30 + "\n")
            print("\nCongratulations! You have achieved your goal!")
            self.goal_met = True
            self.unlock_foyer(game)
          
    def gain_experience(self, difficulty, game):
        experience_points = {"Common": 2, "Uncommon": 3, "Rare": 5}
        self.experience += experience_points[difficulty]
        print(f"\nYou have gained {experience_points[difficulty]} experience points. Total: {self.experience}")
        self.check_for_level_up(game)

    def use_key(self):
      """Use a key to unlock a door."""
      if self.keys > 0:
          self.keys -= 1
          print("You've used a key to unlock the door.")
      else:
          print("You don't have any keys to use.")
  
    def check_for_level_up(self, game):
        levels = {2: 10, 3: 25, 4: 50, 5: 100}  
        for level, threshold in levels.items():
            if self.experience >= threshold and level > self.level:
                self.level = level
                game.level = level
                print(f"\nCongratulations, you've leveled up to Level {self.level}!\n")
                self.choose_stat_increase()
              
    def choose_stat_increase(self):
      skills = [
          "courage",
          "attunement",
          "knowledge",
          "arcane",
          "stealth",
          "investigation",
      ]
      skill_values = {
          "courage": self.courage_value,
          "attunement": self.attunement_value,
          "knowledge": self.knowledge_value,
          "arcane": self.arcane_value,
          "stealth": self.stealth_value,
          "investigation": self.investigation_value,
      }
      for index, skill in enumerate(skills, 1):
          print(f"{index}. {skill.capitalize()}: {skill_values[skill]}")
      choice = int(input("\nEnter the number corresponding to the choice: "))
      if 1 <= choice <= len(skills):
          chosen_skill = skills[choice - 1] + "_value"
          setattr(self, chosen_skill, getattr(self, chosen_skill) + 1)
          print(f"\nYou've increased your {skills[choice - 1].capitalize()} by 1.")
      else:
          print("Invalid choice. Please try again.")

    def use_action(self):
        if self.remaining_actions > 0:
            self.remaining_actions -= 1
        else:
            print("No more actions left this turn.")

    def reset_actions(self):
        self.remaining_actions = self.max_actions

    def end_turn(self,game):
        if self.has_achieved_goal(game):
            print("\nYou have achieved your goal!")
            self.unlock_foyer(game)
        game.turn += 1
        self.reset_actions()

    def receive_new_item(self, new_item):
      print("\n" + "-"*50 + "\n")
      print("You received a reward!\n")
      print(new_item.display())
      if len(self.equipment) < self.equipment_storage:
          new_item.equip(self)  # Equip the new item
      else:
          self.choose_equipment_to_discard(new_item)

    def choose_equipment_to_discard(self, new_item):
      print("\nYou must discard a piece of equipment.\n")
      # List currently equipped items
      equipped_items = self.equipment
      for index, item in enumerate(equipped_items, start=1):
          print(f"{index}. {item.display()}\n")
      print(f"{len(equipped_items)+1}. Discard the new item: {new_item.name} - {new_item.description}")
      choice = input("\nEnter the number of the item to discard/equip: \n")

      # Validate the input
      if choice.isdigit():
          choice = int(choice)
          if 1 <= choice <= len(equipped_items):
              # Discard one of the currently equipped items
              item_to_discard = equipped_items[choice - 1]
              item_to_discard.unequip(self)
              #self.equipment.remove(item_to_discard)
              # Equip the new item if it is not discarded
              if new_item not in self.equipment:
                  new_item.equip(self)
                  #self.equipment.append(new_item)
          elif choice == len(equipped_items) + 1:
              # Discard the new item
              print(f"{new_item.name} was discarded and not equipped.")
          else:
              print("Invalid choice. Please try again.")
              self.choose_equipment_to_discard(new_item)  # Offer the choice again if the input was invalid
      else:
          print("Invalid input. Please enter a number.")
          self.choose_equipment_to_discard(new_item)  # Offer the choice again if the input was invalid
  
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
          
    def add_cleared_location(self,location):
        self.cleared_locations.append(location)

    def view_skills(self):
      skills = ["courage", "attunement", "knowledge", "arcane", "stealth", "investigation"]
      print("\n" + "-"*50 + "\n")
      print("Skills:")
      for index, skill in enumerate(skills, start=1):
          mod_display = ""
          if self.modifiers[skill]:
              mod_display = f" [Currently reduced by {(self.modifiers[skill])*-1}]"
          skill_value = getattr(self, skill + "_value")
          reasoning = getattr(self, skill + "_reasoning")
          print(f"{skill.capitalize()}: {skill_value}{mod_display} - {reasoning}")

      #print(f"Courage: {self.courage_value} Mod: {self.modifiers['courage']} - {self.courage_reasoning}")
      #print(f"Attunement: {self.attunement_value + self.modifiers['attunement']} Mod: {self.modifiers['attunement']} - {self.attunement_reasoning}")
      #print(f"Knowledge: {self.knowledge_value + self.modifiers['knowledge']} Mod: {self.modifiers['knowledge']} - {self.knowledge_reasoning}")
      #print(f"Arcane: {self.arcane_value + self.modifiers['arcane']} Mod: {self.modifiers['arcane']} - {self.arcane_reasoning}")
      #print(f"Stealth: {self.stealth_value + self.modifiers['stealth']} Mod: {self.modifiers['stealth']} - {self.stealth_reasoning}")
      #print(f"Investigation: {self.investigation_value + self.modifiers['investigation']} Mod: {self.modifiers['investigation']} - {self.investigation_reasoning}")
  
    def view_affectations(self):
      print("\n" + "-"*50 + "\n")
      print("Affectations:")
      print(f"Moisture: {self.affectation_moisture_value} - {self.affectation_moisture_reasoning}")
      print(f"Size: {self.affectation_size_value} - {self.affectation_size_reasoning}")
      print(f"Light: {self.affectation_light_value} - {self.affectation_light_reasoning}")
      print(f"Sound: {self.affectation_sound_value} - {self.affectation_sound_reasoning}")

    def view_stats(self,game):
      print("\n" + "-"*50 + "\n")
      print("Stats:")
      print(f"Attempted Encounter Count: {self.attempted_encounter_count}")
      print(f"Cleared Encounter Count: {self.cleared_encounter_count}")
      print(f"Cleared Courage Count: {self.cleared_courage_count}")
      print(f"Cleared Attunement Count: {self.cleared_attunement_count}")
      print(f"Cleared Knowledge Count: {self.cleared_knowledge_count}")
      print(f"Cleared Arcane Count: {self.cleared_arcane_count}")
      print(f"Cleared Stealth Count: {self.cleared_stealth_count}")
      print(f"Cleared Investigation Count: {self.cleared_investigation_count}")
      print(f"Cleared Location Count: {self.cleared_location_count}")
      print(f"Rooms Visited: {self.rooms_visited}/{game.total_locations}")
      
    def view_equipment(self):
        print("\n" + "-"*50 + "\n")
        print ("Your Equipment:\n")
        for idx, item in enumerate(self.equipment, start=1):
          print(f"{idx}. {item.display()}\n")
        print (f"Keys: {self.keys}")

    def view_player(self):
        print("\n" + "-"*50 + "\n")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Goal: {self.goal}")
        print(f"Skill Roll Bonus: {self.modifiers['skillroll']}")
        print(f"Level: {self.level}")
        print(f"Experience: {self.experience}")
        print(f"\nFEAR: {self.fear}")
  
    def player_menu(self,game):
      #Display the character's details and provide options to view Skills, Affectations, and Items.
      self.view_player()

      while True:
        print("\nOptions:")
        print("0. Go Back")
        print("1. View Skills")
        print("2. View Affectations")
        print("3. View Items")
        print("4. View Stats")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            self.view_skills()
        elif choice == "2":
            self.view_affectations()
        elif choice == "3":
            self.view_equipment()
        elif choice == "4":
            self.view_stats(game)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
