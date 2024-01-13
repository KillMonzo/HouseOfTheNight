import json
import random

with open('equipment_dictionary.json', 'r') as file:
  data = json.load(file)

class Item:

    rarities  = ["Common", "Uncommon", "Rare", "Legendary"]
    total_common = 0
    total_uncommon = 0
    total_rare = 0
    total_legendary = 0
  
    def __init__(self, name, description, categories, effect_type, rarity):

        self.name = name
        self.description = description
        self.category1 = categories[0] 
        self.category2 = categories[1] if len(categories) > 1 else None
        self.max_uses = 1
        self.remaining_uses = 1
        self.is_equipped = False
        self.effect_type = effect_type
        self.rarity = "Common"
        self.rarity = self.get_rarity()
        self.effect_value = Item.rarities.index(self.rarity) + 1
      
    def get_rarity(self):
        while True:
            item_rarity = random.choice(Item.rarities)
            if item_rarity == "Common" and Item.total_common <= min(Item.total_uncommon, Item.total_rare, Item.total_legendary):
                Item.total_common += 1
                return item_rarity
            elif item_rarity == "Uncommon" and Item.total_uncommon <= min(Item.total_common, Item.total_rare, Item.total_legendary):
                Item.total_uncommon += 1
                return item_rarity
            elif item_rarity == "Rare" and Item.total_rare <= min(Item.total_common, Item.total_uncommon, Item.total_legendary):
                Item.total_rare += 1
                return item_rarity
            elif item_rarity == "Legendary" and Item.total_legendary <= min(Item.total_common, Item.total_uncommon, Item.total_rare):
                Item.total_legendary += 1
                return item_rarity
  
    def apply_effects(self, player):
      mod = self.effect_type.lower() + "_value"
      current_value = getattr(player, mod, 0)
      setattr(player, mod, current_value + self.effect_value)
    def remove_effects(self, player):
      mod = self.effect_type.lower() + "_value"
      current_value = getattr(player, mod, 0)
      setattr(player, mod, current_value - self.effect_value)
  
    def unequip(self, target):
      self.is_equipped = False
      self.remove_effects(target)
      self.remaining_uses += 1
      target.equipment.remove(self)
      return
          
    def equip(self,target):
      self.is_equipped = True
      self.apply_effects(target)
      target.equipment.append(self)
      self.remaining_uses -= 1
      return
      
    def display(self):
      """Display the item's details."""
      # Construct base information string
      base_info = (
          f"Item Name: {self.name}\n"
          f"Description: {self.description}\n"
          f"Rarity: {self.rarity}\n"
          f"Categories: {self.category1}, {self.category2} \n"
          #f"Type: {self.item_type}\n"
          f"Effect: {self.effect_type} {self.effect_value}"
          #f"Uses Remaining: {self.remaining_uses}/{self.max_uses}\n"
      )
      
      return base_info

with open('equipment_dictionary.json', 'r') as file:
  data = json.load(file)

# Create items
all_items_data = data.get("equipment", [])  # Ensure default to an empty list if "items" key doesn't exist
all_items = [Item(**item) for item in all_items_data]

# Sorting the items by rarity (optional)
common_items = [item for item in all_items if item.rarity == "Common"]
uncommon_items = [item for item in all_items if item.rarity == "Uncommon"]
rare_items = [item for item in all_items if item.rarity == "Rare"]
legendary_items = [item for item in all_items if item.rarity == "Legendary"]

