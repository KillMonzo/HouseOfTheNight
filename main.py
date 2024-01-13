import random

from character import Character
from item import common_items, uncommon_items, rare_items, legendary_items
from location import Location, all_possible_locations
from player import Player

available_locations = all_possible_locations.copy()

class Floor:
  # Add a parameter for the GameState instance
  def __init__(self, name, hall_location, game):
    # no "game" initialization needed here anymore

    global available_locations
    self.name = name
    chosen_locations = random.sample(available_locations, random.randint(4, 5))
    self.locations = [hall_location] + chosen_locations
    for location in chosen_locations:
        available_locations.remove(location)
        game.total_locations += 1
        
class GameState:
  def __init__(self):
      self.turn = 1
      self.level = 1
      self.phase = "New Moon"
      self.phase_desc = "No Effect"
      self.total_locations = 0

      # The Hall replaces The Hall
      self.the_hall = Location(
          name="The Hall",
          description="The central part of the haunted house, with eerie paintings staring down and flickering candles.",
          ambiance="Creaking floorboards, musty smells, and the chill of drafts passing through unseen cracks.",
          affectation_sound_value=0,  # Default values for new affectations
          affectation_moisture_value=0,
          affectation_light_value=0,
          affectation_size_value=0,
          affectation_sound_reasoning="Silence is preserved within the thick walls.",
          affectation_moisture_reasoning="The arid environment keeps moisture away.",
          affectation_light_reasoning="Everlit torches cast a dim glow through the area.",
          affectation_size_reasoning="Ward magic protects against dimensional shifts."
      )
    
      self.the_hall.is_locked = False
      self.active_phenomena = []
      self.item_deck = common_items + uncommon_items + rare_items  # This would be populated with new themed items
      self.floors = ["Cellar", "First Floor", "Second Floor", "Third Floor", "Attic"]  # Example floor names
      self.floors = [Floor(name, self.the_hall, self) for name in self.floors]
      self.current_floor = self.floors[1]  # Start on the first floor
      self.current_location = self.the_hall  # Start at The Hall

  def update_game_phase(self):
    phases = ["New Moon", "Half Moon", "Full Moon"]
    descs = ["No Effect", "Player rolls d5 instead of d6", "Phenomena roll d7 instead of d6"]
    current_phase_index = phases.index(self.phase)
    self.phase = phases[(current_phase_index + 1) % len(phases)]
    self.phase_desc = descs[(current_phase_index + 1) % len(phases)]

def go_to_location(player,game,location):
    player.current_location = location
    player.use_action()
    hallway_art = """
    ___________
    |  __  __  |
    | |  ||  | |
    | |  ||  | |
    | |__||__| |
    |  __  __()|
    | |  ||  | |
    | |  ||  | |
    | |  ||  | |
    | |__||__| |
    |__________|
    """

    print(hallway_art)
    main_actions(player,game)
      
def navigation_panel(player, game):
  accessible_locations = [location for location in game.current_floor.locations if location.name != player.current_location.name and not location.is_locked]
  locked_locations = [location for location in game.current_floor.locations if location.is_locked]

  print("\n" + "-"*50 + "\n")
  print("Leave Move:")
  print("0. Go Back")
  print("\nEnter A Room:")
  for i, location in enumerate(accessible_locations, 1):
      visited  = "VISITED - " if location.is_visited and not location.name in player.cleared_locations else ""
      status = " (Cleared)" if location.name in player.cleared_locations else ""
      print(f"{i}. {visited}{location.name}{status}")
  for i, location in enumerate(locked_locations, len(accessible_locations) + 1):
      print(f"{i}. {location.name} (Locked)")
  current_floor_idx = game.floors.index(game.current_floor)
  floor_choice_start_index = len(accessible_locations) + len(locked_locations) + 1
  print("\nChange Floors:")

  if current_floor_idx > 0:
      print(f"{floor_choice_start_index}. Go down to {game.floors[current_floor_idx - 1].name}")
  if current_floor_idx < len(game.floors) - 1:
      print(f"{floor_choice_start_index + (1 if current_floor_idx > 0 else 0)}. Go up to {game.floors[current_floor_idx + 1].name}")

  choice = input("Enter your choice: ")
  if choice.isdigit():
      choice = int(choice)
      total_locations = len(accessible_locations) + len(locked_locations)
      if 1 <= choice <= total_locations:
          idx = choice - 1
          if idx < len(accessible_locations):
              selected_location = accessible_locations[idx]
              go_to_location(player, game, selected_location)
          else:
              selected_location = locked_locations[idx - len(accessible_locations)]
              if player.keys > 0:
                  print(f"\nYou have {player.keys} key(s) available.")
                  use_key = input(f"Would you like to use a key to unlock {selected_location.name}?\n0. No\n1. Yes\n").lower().strip()
                  if use_key == "1":
                      player.use_key()
                      selected_location.is_locked = False
                      go_to_location(player, game, selected_location)
                  elif use_key == "0":
                      return
                      #main_actions(player, game) 
                  else:
                      print("\nInvalid choice.")
                      return
              else:
                  print("\nYou do not have a key to unlock this location.")
                  input("Press Enter to continue...")
                
      elif choice == floor_choice_start_index and current_floor_idx > 0:
          game.current_floor = game.floors[current_floor_idx - 1]
          player.current_location = game.the_hall
          print(f"You moved to {game.current_floor.name}.")
      elif choice == floor_choice_start_index + (1 if current_floor_idx > 0 else 0) and current_floor_idx < len(game.floors) - 1:
          game.current_floor = game.floors[current_floor_idx + 1]
          player.current_location = game.the_hall
          print(f"You moved to {game.current_floor.name}.")
      elif len(locked_locations) > 0 and choice <= len(locked_locations) + len(accessible_locations):
          print("That location is locked. You cannot enter it.")
      elif choice == 0:
          return
      else:
          print("Invalid choice, please try again.")
          navigation_panel(player, game)
  else:
      print("Invalid input, please enter a number.")
      navigation_panel(player, game)

def main_actions(player, game):
  player.current_location.clear_check(player,game)
  
  print("\n" + "-"*50 + "\n")
  print(f"Phase: {game.phase}")
  print(f"Turn: {game.turn}")
  print(f"Actions remaining: {player.remaining_actions}")
  print(f"Current floor: {game.current_floor.name}\n")
  player.current_location.display_location(player)
  print ("\n1. View Player Panel")
  print ("2. Move (Cost: 1 Action)")
  
  if player.current_location.name == "The Hall":
      choice = input("\nEnter your choice: \n")
      if choice == "1":
        player.player_menu(game)
        return
      elif choice == "2":
        navigation_panel(player, game)
  else:
      inactive_phenomena = [p for p in player.current_location.phenomena if not p.active]
      active_phenomena = [p for p in player.current_location.phenomena if p.active]
      
      if len(inactive_phenomena) > 0:
            print("3. Activate Next Phenomenon (Cost: 1 Action)")
            print(f"4. Interact With Active Phenomena: {len(active_phenomena)}")
            choice = input("\nEnter your choice: \n")
        
            if choice == "1":
              player.player_menu(game)
              return
              
            elif choice == "2":
              navigation_panel(player, game)
              
            elif choice == "3":  # Activation of next phenomenon
                player.current_location.activate_next_phenomenon(player)
                print("Next phenomenon has been activated.")
                player.use_action()
                return
              
            elif choice == "4":  # Interaction with active phenomena
              if len(active_phenomena) > 1:
                print("\nChoose an active phenomenon to interact with:")
                for index, active_phen in enumerate(active_phenomena, start=1):
                    print(f"{index}. {active_phen.name} - {active_phen.associated_skill}")
                phen_choice = input("\nEnter the number of the phenomenon: ")
                if phen_choice.isdigit(): 
                    phen_choice = int(phen_choice)
                    phen_choice -= 1
                    if 0 <= phen_choice < len(active_phenomena):
                        active_phenomena[phen_choice].interact(player, game)
                else:
                    print("Invalid choice.")
              else:
                player.current_location.phenomena[0].interact(player,game)
            else:
                print("Invalid choice or no action available for this option.")
            
      else:
            print(f"3. Interact With Active Phenomena: {len(active_phenomena)}")
            print("\nAll Phenomena Active!")
            choice = input("\nEnter your choice: \n")
            if choice == "1":
              player.player_menu(game)
            elif choice == "2":
              navigation_panel(player, game)
            elif choice == "3":  # Interaction with active phenomena
              if len(active_phenomena) > 1:
                print("\nChoose an active phenomenon to interact with:")
                for index, active_phen in enumerate(active_phenomena, start=1):
                    print(f"{index}. {active_phen.name} - {active_phen.associated_skill}")
                phen_choice = input("\nEnter the number of the phenomenon: ")
                if phen_choice.isdigit(): 
                    phen_choice = int(phen_choice)
                    phen_choice -= 1
                    if 0 <= phen_choice < len(active_phenomena):
                        active_phenomena[phen_choice].interact(player, game)
                else:
                    print("Invalid choice.")
              else:
                player.current_location.phenomena[0].interact(player,game)
          
            else:
                print("Invalid choice.")
              
  player.check_for_goal(game)
  
def spawn(game):
    # Generate 5 random characters
    random_characters = [Character() for _ in range(5)]

    # Display them to the player
    print("Choose your character:\n")
    for index, character in enumerate(random_characters, start=1):
        print(f"Character {index}:")
        print(character.display())
        #print("\n" + "-"*50 + "\n")
        print("-"*50)

    # Item rarity distribution test
    #print(f"{len(common_items)} common items available.")
    #for i in range(len(common_items)):
    #  print(f"{common_items[i].name} - {common_items[i].rarity}")
    #print(f"{len(uncommon_items)} uncommon items available.")
    #for i in range(len(uncommon_items)):
    #  print(f"{uncommon_items[i].name} - {uncommon_items[i].rarity}")
    #print(f"{len(rare_items)} rare items available.")
    #for i in range(len(rare_items)):
    #  print(f"{rare_items[i].name} - {rare_items[i].rarity}")
    #print(f"{len(legendary_items)} legendary items available.")
    #for i in range(len(legendary_items)):
    #  print(f"{legendary_items[i].name} - {legendary_items[i].rarity}")
      
    choice = input("Enter the number corresponding to your choice (1-5): \n")
  
    if not choice.isdigit() or int(choice) < 0 or int(choice) > 5:
        print("Invalid choice.")
        return spawn(game)
    else:
        chosen_character = random_characters[int(choice) - 1]
        print("\nYou have chosen:")
        player = Player(chosen_character)
        starting_item = random.choice(uncommon_items)
        starting_item.equip(player)
        uncommon_items.remove(starting_item)
      
        player.current_location = game.current_location
        #player.player_menu()
        player.view_player()
        player.view_skills()
        player.view_affectations()
        player.view_equipment()
        choice = input(f"\nProceed with {player.name}?\n\n0. Go Back\n1. Proceed\n")
        if choice == "1":
                # Set to "The Hall" in "Alpha"
              return player
        elif not choice.isdigit() or int(choice) != 0:
              print("Invalid choice.")
              uncommon_items.append(starting_item)
              return spawn(game)
        else:
              uncommon_items.append(starting_item)
              return spawn(game)

def main():
    game = GameState()
    # Character selection
    print("Welcome to the House Of The Night")
    house_image = r"""
                               .-----.
                             .'       `.
                            :      ^v^  :
                            :           :
                            '           '
             |~        www   `.       .'
            /.\       /#^^\_   `-/\--'
           /#  \     /#%    \   /# \
          /#%   \   /#%______\ /#%__\
         /#%     \   |= I I ||  |- |
         ~~|~~~|~~   |_=_-__|'  |[]|
           |[] |_______\__|/_ _ |= |`.
    ^V^    |-  /= __   __    /-\|= | :;
           |= /- /\/  /\/   /=- \.-' :;
           | /_.=========._/_.-._\  .:'
           |= |-.'.- .'.- |  /|\ |.:'
           \  |=|:|= |:| =| |~|~||'|
            |~|-|:| -|:|  |-|~|~||=|      ^V^
            |=|=|:|- |:|- | |~|~|| |
            | |-_~__=_~__=|_^^^^^|/___
            |-(=-=-=-=-=-(|=====/=_-=/\
            | |=_-= _=- _=| -_=/=_-_/__\ 
            | |- _ =_-  _-|=_- |]#| I II
            |=|_/ \_-_= - |- = |]#| I II
            | /  _/ \. -_=| =__|]!!!I_II!!
           _|/-'/  ` \_/ \|/' _ ^^^^`.==_^.
         _/  _/`-./`-; `-.\_ / \_'\`. `. ===`.
        / .-'  __/_   `.   _/.' .-' `-. ; ====;\
       /.   `./    \ `. \ / -  /  .-'.' ====='  >
      /  \  /  .-' `--.  / .' /  `-.' ======.' /
      
    """
    print(house_image)
    input("Press Enter to continue...")
    player = spawn(game)

    while True:
        if player.remaining_actions == 0:
          print("\n" + "*-"*30 + "\n")
          print("You have no more actions left this turn.")
          print(f"\nThe {game.phase} phase passes.")
          player.end_turn(game)
          game.update_game_phase()  # Update to the next game phase at the end of the turn
          print(f"\nThe {game.phase} phase begins.")
          print(game.phase_desc)
          input("\nPress ENTER to end the turn.")
        if player.fear >= 5:
          print("\n" + "*-"*30 + "\n")
          print("You have succumbed to fear and are consumed into The House of the Night.")
          print("Game Over.")
          break
        if player.goal_met:
          print("Congratulations! You open the door and escape The House of the Night.")
          print("\nYou have won the game.")
          break
        main_actions(player, game)
      
if __name__ == "__main__":
    main()