import json
import random

from ascii_art import AsciiArt
from item import legendary_items
from phenomenon import Phenomenon, phenomenon_data

# Here we assume that ascii_art.py contains a class AsciiArt with all the ASCII images.
ascii_art = AsciiArt()

# Load affectation data and locations from JSON
with open('location_dictionary.json', 'r') as file:
    locations_data = json.load(file)
    #locations_data = data['locations']

drawn_phenomena_ids = set()

# Class for Location
class Location:
  def __init__(self, name, description, ambiance, affectation_moisture_value, affectation_moisture_reasoning, affectation_size_value, affectation_size_reasoning, affectation_light_value, affectation_light_reasoning, affectation_sound_value, affectation_sound_reasoning):
    
            self.name = name
            self.description = description
            self.ambiance = ambiance
            self.affectation_moisture_value = affectation_moisture_value
            self.affectation_moisture_reasoning = affectation_moisture_reasoning
            self.affectation_size_value = affectation_size_value
            self.affectation_size_reasoning = affectation_size_reasoning
            self.affectation_light_value = affectation_light_value
            self.affectation_light_reasoning = affectation_light_reasoning
            self.affectation_sound_value = affectation_sound_value  
            self.affectation_sound_reasoning = affectation_sound_reasoning
            self.image = ascii_art.get_ascii_image(self.name)

            self.courage_mod = 0
            self.attunement_mod = 0
            self.arcane_mod = 0
            self.knowledge_mod = 0
            self.stealth_mod = 0
            self.investigation_mod = 0
            self.moisture_mod = 0
            self.size_mod = 0
            self.light_mod = 0
            self.sound_mod = 0
            self.actions_mod = 0
            self.skillroll_mod = 0
    
            self.phenomena = []
            self.is_visited = False

            self.is_locked = self.locked_or_unlocked()

  def locked_or_unlocked(self):
    lock_percentage = random.randint(0, 100)
    return lock_percentage < 30
  
  def display_location(self, player):
    # Display location details
    #print(self.image)
    print(f"Location: {self.name}")
    print(f"Description: {self.description}")
    print(f"Ambiance: {self.ambiance}\n")
    # Display affectations, ensuring they are within the limits
    

    #print(f"\nCourage Mod: {self.courage_mod}")
    #print(f"Attunement Mod: {self.attunement_mod}")
    #print(f"Arcane Mod: {self.arcane_mod}")
    #print(f"Knowledge Mod: {self.knowledge_mod}")
    #print(f"Stealth Mod: {self.stealth_mod}")
    #print(f"Investigation Mod: {self.investigation_mod}")
      
    if self.name != "The Hall":
          print("")
    if self.phenomena:  
          self.mod_display(player)
          print(f"\nActive Phenomena ({len(self.phenomena)} total) :")
          for phenomenon in self.phenomena:
            if phenomenon.active:

                if phenomenon.effect_desc in (['Size','Moisture','Light','Sound']) and phenomenon.effect_value >= 0:
                      print(f"- {phenomenon.name}: - {phenomenon.associated_skill} | Effect: +{phenomenon.effect_value} {phenomenon.effect_desc}") 
                elif phenomenon.effect_desc in (['Size','Moisture','Light','Sound']) and phenomenon.effect_value < 0:
                      print(f"- {phenomenon.name}: - {phenomenon.associated_skill} | Effect: {phenomenon.effect_value} {phenomenon.effect_desc}")
                else:
                      print(f"- {phenomenon.name}: - {phenomenon.associated_skill} | Effect: -{phenomenon.effect_value} {phenomenon.effect_desc}")
          
  def activate_next_phenomenon(self,player):
    """Activate the next inactive phenomenon."""
    for phenomenon in self.phenomena:
        if not phenomenon.active:
            phenomenon.activate(self,player)
            break  # Stop after activating one phenomenon

  def draw_phenomena(self, player):
    
    # Number of phenomena to draw
    num_phenomena = random.randint(4, 6)  # Or your own logic to determine the number
    # Getting distribution values based on the player's level
    distribution = {
      1: ('Common4', 0.6, 'Common5', 0.2, 'Common6', 0.1, 
          'Uncommon7', 0.06, 'Uncommon8', 0.025, 'Uncommon9', 0.015),
      2: ('Common4', 0.035, 'Common5', 0.065, 'Common6', 0.2, 
          'Uncommon7', 0.3, 'Uncommon8', 0.2, 'Uncommon9', 0.1, 
          'Rare10', 0.06, 'Rare11', 0.025, 'Rare12', 0.015),
      3: ('Uncommon7', 0.1, 'Uncommon8', 0.3, 'Uncommon9', 0.2, 
          'Rare10', 0.02, 'Rare11', 0.015, 'Rare12', 0.005),
      4: ('Uncommon7', 0.01, 'Uncommon8', 0.04, 'Uncommon9', 0.15, 
        'Rare10', 0.25, 'Rare11', 0.4, 'Rare12', 0.15),
      5: ('Rare', 1.0)
    }
    player_level = player.level  # Assuming player level attribute is available
    diff_distribution = distribution.get(player_level, ('Common4', 1.0))
    # Dividing keys and weights for choices
    difficulty_keys = diff_distribution[::2]
    difficulty_weights = diff_distribution[1::2]
    self.phenomena = []  # Clear current phenomena
    for _ in range(num_phenomena):
        # Choose a random difficulty according to weights
        difficulty = random.choices(difficulty_keys, weights=difficulty_weights, k=1)[0]
        all_pheno_ids = set(phenomenon_data.keys())  # All possible phenomena IDs
        available_pheno_ids = all_pheno_ids - drawn_phenomena_ids

        if available_pheno_ids:
              pheno_id = random.choice(list(available_pheno_ids))
              drawn_phenomena_ids.add(pheno_id)  # Add to the set of drawn phenomena ID
              # Instantiate the Phenomenon object with the chosen ID
              pheno = Phenomenon(pheno_id, difficulty)
              self.phenomena.append(pheno)
        else:
              # If no available IDs, break from the loop
              break

    if self.phenomena:
          self.phenomena[0].activate(self, player)
      
  def clear_check(self,player,game):
      if self.name != "The Hall":  
        if not player.current_location.is_visited:
            self.draw_phenomena(player)
            player.current_location.is_visited = True
            player.rooms_visited += 1
          
        if not self.phenomena:  # The location is clear
            player.add_cleared_location(self.name)
            player.cleared_location_count += 1
            print(f"\nLocation '{self.name}' has been cleared of all phenomena!")
          
            if not legendary_items:
              print("\nNo Legendary items left!")
            else:
              reward_item = random.choice(legendary_items)
              legendary_items.remove(reward_item)
              print(f"\nCongratulations! You've received an Legendary item: {reward_item.name}")
              player.receive_new_item(reward_item)
            print("\nYou are now back at 'The Hall'")
            player.current_location = game.the_hall
            return True
        else:
            self.phenomena[0].activate(self,player)
            return False    

  def mod_display(self, player):
      #print("Running mod_display")

      attributes = [
        'moisture', 'light', 'size', 'sound'
      ]
    
      for attr in attributes:
        # Get the affectation value and mod from the location
        value = getattr(self, f"affectation_{attr}_value", 0)
        mod = getattr(self, f"{attr}_mod", 0)
        # Calculate the total affectation value
        total_value = value + mod
        # Apply the limits
        total_value = max(-5, min(total_value, 5))
        # Retrieve the reasoning for display
        reasoning = getattr(self, f"affectation_{attr}_reasoning", "")
        # Display the adjusted affectation and reasoning
        print(f"{attr.capitalize()}: {value + mod} - {reasoning}")
       # Sums are already handled in the display, no need to re-calculate or access player properties
      # Create flags to indicate when to produce a warning
      moisture_warning = self.affectation_moisture_value + self.moisture_mod + player.affectation_moisture_value
      light_warning = self.affectation_light_value + self.light_mod + player.affectation_light_value
      size_warning = self.affectation_size_value + self.size_mod + player.affectation_size_value
      sound_warning = self.affectation_sound_value + self.sound_mod + player.affectation_sound_value
      
      warnings = []
      
      if moisture_warning >= 5:
          warnings.append(f"MOISTURE LIMIT REACHED! You are affected by extreme moisture! Your Attunement skill is reduced by {moisture_warning - 4}!")
      elif moisture_warning <= -5:
          warnings.append(f"MOISTURE LIMIT REACHED! You are affected by extreme moisture! Your Knowledge skill is reduced by {(moisture_warning + 4) * -1}!")
      if light_warning >= 5:
          warnings.append(f"LIGHT LIMIT REACHED! You are affected by extreme light! Your Arcane skill is reduced by {light_warning - 4}!")
      elif light_warning <= -5: 
          warnings.append(f"LIGHT LIMIT REACHED! You are affected by extreme light! Your Fear is increased by {(light_warning + 4)*-1}!")
      if size_warning >= 5:
          warnings.append(f"SIZE LIMIT REACHED! You are affected by extreme size! Your Investigation skill is reduced by {size_warning - 4}!")
      elif size_warning <= -5:
          warnings.append(f"SIZE LIMIT REACHED! You are affected by extreme size! Action points reduced by {(size_warning + 4)*-1}!")
      if sound_warning >= 5:
          warnings.append(f"SOUND LIMIT REACHED! You are affected by extreme sound! Your Stealth skill is reduced by {sound_warning - 4}!")
      elif sound_warning >= 5:
          warnings.append(f"SOUND LIMIT REACHED! You are affected by extreme sound! Your Courage skill is reduced by {(sound_warning + 4)*-1}!")
          #for skill in ['courage', 'attunement', 'knowledge', 'arcane', 'stealth', 'investigation']:
          #player.modifiers[skill] -= 1

      for warning in warnings:
        print(f"WARNING: {warning}")
        
      # Check for any active mod effects due to phenomena
      any_mod_active = any([
        self.courage_mod, self.attunement_mod, self.knowledge_mod, self.arcane_mod, self.investigation_mod, self.stealth_mod, self.sound_mod, self.size_mod, self.moisture_mod, self.light_mod])
      
      if any_mod_active:
          print("\nPhenomena Effects Active!")
          for effect in ['courage', 'attunement', 'knowledge', 'arcane', 'stealth', 'investigation','sound', 'size', 'moisture', 'light', 'actions', 'skillroll']:
              mod_value = getattr(self, f"{effect}_mod")
              if mod_value:
                  print(f"{effect.capitalize()} {mod_value}")  # Formatted to show positive/negative
      
  def phenomenon_effect(self, phenomenon, player, add_or_remove):

    moisture_warning = self.affectation_moisture_value - self.moisture_mod + player.affectation_moisture_value
    light_warning = self.affectation_light_value - self.light_mod + player.affectation_light_value
    size_warning = self.affectation_size_value - self.size_mod + player.affectation_size_value
    sound_warning = self.affectation_sound_value - self.sound_mod + player.affectation_sound_value
    result = ["",0]

    mod = phenomenon.effect_desc.lower()
    mod_key = mod + '_mod'
    affectation_skill = ""
    affectation_value = 0

    if add_or_remove == 'add':
      #print(f"adding phenomena value {phenomenon.effect_value} to location mod {self.mod_key}")
      
      current_value = getattr(self, mod_key)
      setattr(self, mod_key, current_value + phenomenon.effect_value)

      if moisture_warning >= 5:
          affectation_skill = 'attunement'
          affectation_value = moisture_warning - 4
      elif moisture_warning <= -5:
          affectation_skill = 'knowledge'
          affectation_value = (moisture_warning + 4) * -1
      if light_warning >= 5:
          affectation_skill = 'arcane'
          affectation_value = light_warning - 4
      elif light_warning <= -5:
          affectation_skill = 'fear'
          affectation_value = (light_warning + 4)*-1
      if size_warning >= 5:
          affectation_skill = 'investigation'
          affectation_value = size_warning - 4
      elif size_warning <= -5:
          affectation_skill = 'actions'
          affectation_value = (size_warning + 4)*-1
      if sound_warning >= 5:
          affectation_skill = 'stealth'
          affectation_value = sound_warning - 4
      elif sound_warning <= -5:
          affectation_skill = 'courage'
          affectation_value = (sound_warning + 4)*-1

      #if affectation_skill and affectation_value:
      #  if affectation_skill == 'fear':
      #      player.fear += affectation_value
      #  elif affectation_skill == 'actions':
      #      player.max_actions -= affectation_value
      #  else:
      #      player.modifiers[affectation_skill] -= affectation_value
  
      if affectation_skill != "" and affectation_value != 0:
          print (f"{result[0].capitalize()} lowered by {result[1]}")
          
    elif add_or_remove == 'remove':
      current_value = getattr(self, mod_key)
      setattr(self, mod_key, current_value - phenomenon.effect_value)

      #if mod in player.modifiers:
      #    player.modifiers[mod] += phenomenon.effect_value
      
      #if phenomenon.effect_desc in player.modifiers:
      #    player.modifiers[phenomenon.effect_desc] += phenomenon.effect_value
      #if affectation_skill and affectation_value:
      #  if affectation_skill == 'fear':
      #        player.fear -= affectation_value
      #  elif affectation_skill == 'actions':
      #        player.max_actions += affectation_value
      #  else:
      #        player.modifiers[affectation_skill] += affectation_value
  
all_possible_locations = [Location(
           name=location_info['name'],
           description=location_info['description'],
           ambiance=location_info['ambiance'],
           affectation_size_value=location_info['affectation_size_value'],
           affectation_size_reasoning=location_info['affectation_size_reasoning'],
           affectation_moisture_value=location_info['affectation_moisture_value'],
           affectation_moisture_reasoning=location_info['affectation_moisture_reasoning'],
           affectation_light_value=location_info['affectation_light_value'],
           affectation_light_reasoning=location_info['affectation_light_reasoning'],
           affectation_sound_value=location_info['affectation_sound_value'],
           affectation_sound_reasoning=location_info['affectation_sound_reasoning'])
           
 for location_info in locations_data.values()]