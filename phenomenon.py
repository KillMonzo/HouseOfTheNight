import json
import random

from entity import Entity
from item import common_items, rare_items, uncommon_items 

# Initialize an empty master dictionary
phenomenon_data = {}
# List of JSON files for each type of phenomenon
phenomenon_files = [
    'arcane_phenomenon_dictionary.json',
    'attunement_phenomenon_dictionary.json',
    'courage_phenomenon_dictionary.json',
    'investigation_phenomenon_dictionary.json',
    'knowledge_phenomenon_dictionary.json',
    'stealth_phenomenon_dictionary.json'
]
# Load data from each file and add it to the master dictionary
for file_name in phenomenon_files:
    with open(file_name, 'r') as file:
        data = json.load(file)
        # If you are sure that keys are unique across dictionaries, you can update the master dictionary directly.
        # Otherwise, consider a strategy to handle duplicate keys.
        phenomenon_data.update(data)

class Phenomenon:

  def __init__(self, phenomenon_id,difficulty):
    #print(phenomenon_data)
    self.data = phenomenon_data[str(phenomenon_id)]
    #[phenomenon_id]
    #self.entity = Entity()
    self.name = self.data["name"]
    self.description = self.data["description"]
    self.effect_desc = random.choice(["Courage" , "Attunement" , "Knowledge" , "Arcane" , "Stealth", "Investigation", "SkillRoll", "Actions", "Moisture", "Size", "Light", "Sound"])
    #self.effect_value = 0
    self.resolution = self.data["resolution"]
    self.difficulty = difficulty
    self.applied_effects = []
    
    if self.difficulty == "Common4":
      self.skill_check = 4
      self.difficulty = "Common"
    elif self.difficulty == "Common5":
      self.skill_check = 5
      self.difficulty = "Common"
    elif self.difficulty == "Common6":
      self.skill_check = 6
      self.difficulty = "Common"
    elif self.difficulty == "Uncommon7":
      self.skill_check = 7
      self.difficulty = "Uncommon"
    elif self.difficulty == "Uncommon8":
      self.skill_check = 8
      self.difficulty = "Uncommon"
    elif self.difficulty == "Uncommon9":
      self.skill_check = 9
      self.difficulty = "Uncommon"
    elif self.difficulty == "Rare10":
      self.skill_check = 10
      self.difficulty = "Rare"
    elif self.difficulty == "Rare11":
      self.skill_check = 11
      self.difficulty = "Rare"
    elif self.difficulty == "Rare12":
      self.skill_check = 12
      self.difficulty = "Rare"

    if self.difficulty == "Common":
      self.effect_value = random.randint(1,2)
    elif self.difficulty == "Uncommon":
      self.effect_value = random.randint(3,4)
    elif self.difficulty == "Rare":
      self.effect_value = random.randint(5,6)

    if self.effect_desc in ["Moisture", "Light", "Size", "Sound"]:
      self.effect_value = self.effect_value * random.choice([-1,1])
  
    self.associated_skill = self.data["associated_skill"]
    self.secondary_requirement = self.data["secondary_requirement"]
    self.resolved = False
    self.active = False
      
  def meets_secondary_requirement(self, player):
    """Check if the player has the required item."""
    required_item_type = self.secondary_requirement
    return any(required_item_type == item.category1 or required_item_type == item.category2 for item in player.equipment)

  def arcane_encounter(self, player, game):
    
    entity = Entity("Arcane")
    print(f"\n{'*'*100}\nArcane Encounter: {self.name}\n{'*'*100}\n")
    print(f"In the midst of an arcane storm, {entity.name} emerges, shackled in forbidden magic!\n")
    player_arcane_value = player.arcane_value + player.modifiers.get('arcane', 0)  # Assumes player has 'arcane' attribute
    # Apply location modifier
    location_mod = player.current_location.arcane_mod
    player_arcane_value -= location_mod
    challenge_level = self.skill_check
    print(f"{player.name} | Arcane Power: {player_arcane_value}")
    print(f"{entity} | Arcane Power: {challenge_level}")
    input("\n-Press ENTER to cast your arcane defenses...")
    while player_arcane_value > 0 and challenge_level > 0:
        player_roll = self._roll(game,"Player",player)  # Player's d6 roll
        phenomenon_roll = self._roll(game,"Phenomenon",player) # Entity's d6 roll
        print(f"\n{'- - '*20}\n")
        print(f"You roll: {player_roll + player_arcane_value}")
        print(f"{entity.name} rolls: {phenomenon_roll}\n")
        # Player's attempt to overcome the arcane challenge
      
        if player_roll + player_arcane_value > phenomenon_roll:
        #if player_roll >= entity_roll:
            challenge_level -= 1
            print("You counter the arcane forces with your knowledge, getting one step closer to victory!\n")
        elif player_roll + player_arcane_value == phenomenon_roll:
            print("Your forces are equally matched, and you continue to fight!\n")
        else:
            player_arcane_value -= 1
            print("The entity's power proves too strong this round, and it takes a toll on your arcane resources.\n") 
        #challenge_level -= 1
        # Show remaining challenge and player's arcane strength after each round
        #print(f"Remaining Challenge Level: {challenge_level}")
        print(f"{player.name} | Arcane Power: {player_arcane_value}")
        print(f"{entity} | Arcane Power: {challenge_level}")
        if challenge_level != 0 and player_arcane_value !=0 :
          input("\n-Press ENTER to continue the encounter...")

    # Determine and display the outcome
    if challenge_level == 0:
        print(f"\n{'-'*100}\n")
        print(f"{player.name} has successfully subdued the mystical forces, winning the arcane duel!")
        result = True   # Player wins
    else:
        print(f"\n{'-'*100}\n")
        print(f"{player.name} has been overwhelmed by the arcane entity.")
        #input("\n-Press ENTER to end the encounter...")
        result = False  # Entity wins
      
    return result

  def attunement_encounter(self, player, game):
    #player.use_action()
    print(f"\n{'*'*100}\nAttunement Encounter: {self.name}!\n{'*'*100}")
    rounds_to_attune = self.skill_check  # The number of rounds the player must succeed to attune
    percentage = 100/rounds_to_attune  # Percentage of success required to attune
    total_percentage = 0
    player_attunement_value = player.attunement_value + player.modifiers['attunement']
    location_mod = player.current_location.attunement_mod
    player_attunement_value -= location_mod
    resistance = player_attunement_value
    success = True  # Initial assumption
    print(f"\nAttune to the spiritual or psychic vibrations within {rounds_to_attune} rounds.")
    print(f"Your Attunement Skill Level: {player_attunement_value}.")
    input(f"\n-Press ENTER to begin attunement...")

    # Messages for attunement encounter 
    attunement_messages = [
        "You sense a cold draft, as if the spectral embrace of the abyss is near.",
        "In the oppressive silence, ancient whispers crawl into your consciousness.",
        "A thick fog of dread enfolds you, challenging your resolve to connect with the beyond.",
        "The heavy air carries a sorrowful lament, a remnant of a once tormented soul.",
        "Shadows lengthen, and from the corners of your sight, you glimpse fleeting figures of darkness.",
        "The insidious chill of the otherworld seeps into your bones, testing your spirit.",
        "A shudder runs through you as the line between life and death momentarily thins.",
        "The very essence of the night conspires with you, invoking arcane truths known to the departed.",
        "Visions of a forgotten past flash before your eyes, bidding you to understand their mysteries.",
        "An almost imperceptible melody of the dammed beckons you towards the ethereal plane.",
        "You feel an invisible weight upon your chest, as if the air is thick with unspoken secrets.",
        "Dim, ghostly lights flicker as though signaling from a realm drenched in sorrow.",
        "A silent wail of anguish resonates deep within, guiding you through the shades of despair.",
        "Mournful echoes surround you, coiling tighter with each breath you take towards attunement.",
        "The world darkens, and for a moment, you tread the liminal space where spirits dwell.",
        "A spectral touch grazes your thoughts, leaving behind a trace of timeless knowledge.",
        "Whispers of the doomed intertwine with your own heartbeat, drawing you deeper into shadow."
        # Add more messages as desired...
    ]
    for round_number in range(1, rounds_to_attune + 1):
        player_roll = self._roll(game,"Player",player)  # Player's d6 roll
        phenomenon_roll = self._roll(game,"Phenomenon",player) # Entity's d6 roll
        player_roll += player_attunement_value
        print(f"\n{'- - '*20}\n")
        print(f"Round {round_number}:")
        print(f"{player.name} rolled a {player_roll}.")
        print(f"{self.name} rolled a {phenomenon_roll}.")
        total_percentage += percentage
        if player_roll < phenomenon_roll:
            resistance -= 1
            if resistance <= 0:
                print(f"You lose the connection and fail to attune with {self.name}. The encounter is lost.")
                success = False
                input("\n-Press ENTER to end the encounter...")
                return success
            else:
                if round_number < rounds_to_attune:  # Check if it's not the last round
                  print("\nYou struggle to connect with the spiritual forces at play and your connections wavers.")
                  print(f"Your Attunement Skill Level: {resistance}.")
                  print("Attunement - Bond Weakens")
                  input("\n-Press ENTER to further attune...\n")
        else:
            # Select a random survival message
            message = random.choice(attunement_messages)
            print(f"\n{message}\n")
            print(f"Your Attunement Skill Level: {resistance}.")
            #print("Attunement - Bond Complete!")
            if round_number < rounds_to_attune:  # Check if it's not the last round
                print(f"Attunement - Bond Strengthens - {total_percentage}%")
                input("\n-Press ENTER to further attune...\n")
            if round_number == rounds_to_attune:
                print(f"Attunment - Bond Complete! - {total_percentage}%")
    if success:
        print(f"\n{'-'*100}\n")
        print(f"Player successfully attuned with {self.name}!")
    return success
    
  def courage_encounter(self, player, game):
    #player.use_action()
    entity = Entity("Phantom")
    print(f"\n{'*'*100}\nCourage Encounter: {self.name}\n{'*'*100}\n")
    print(f"{self.name} summons an ENTITY!\n{entity.name} appears! Staring into the abyss, can you withstand the terror?")
    input("\n-Press ENTER to continue...")
    player_courage_value = player.courage_value + player.modifiers.get('courage', 0)
    location_mod = player.current_location.courage_mod
    player_courage_value -= location_mod
    scores = {'player': 0, 'phenomenon': 0}
    player_text_options = [
        "You shout a defiant challenge against the darkness.",
        "You stand resolute, eyes burning with determination.",
        "Your battlecry echoes, bolstering your spirit.",
        "Taking a deep breath, you steel yourself against fear.",
        "With a stony gaze, you face the entity head-on.",
        "You shout your battle cry, screaming for mercy.",
        "You stand firm, courageous, brave, and confident."
        # Add more options as desired.
    ]
    entity_text_options = [
        f"{entity.name} emanates an aura of sheer terror",
        f"The air grows cold as {entity.name} approaches.",
        f"{entity.name} lets out a bloodcurdling howl.",
        f"A malevolent force radiates from {entity.name}.",
        f"Eerie whispers surround you as {entity.name} tries to invade your mind.",
        f"{entity.name} screams in pain, screaming for mercy"
        
        # Add more options as desired.
    ]
    while scores['player'] < 3 and scores['phenomenon'] < 3:
        player_roll = self._roll(game,"Player",player)  # Player's d6 roll
        phenomenon_roll = self._roll(game,"Phenomenon",player) # Entity's d6 roll  # Player's d6 roll
        player_roll += player_courage_value
        print(f"\n{'- - '*20}\n")
        print(f"You roll: {player_roll}")
        print(f"{entity.name} rolls: {phenomenon_roll}")

        if player_roll >= phenomenon_roll:
            scores['player'] += 1
            print(random.choice(player_text_options))
            input("\n-Press ENTER to steel yourself for the next round...")
        else:
            scores['phenomenon'] += 1
            print(random.choice(entity_text_options))
            input("\n-Press ENTER to steel yourself for the next round...")
    if scores['player'] == 3:
        print(f"\n{'-'*100}\n")
        print(f"You have outlasted the terror of {entity.name}.")
        return True
    else:
        print(f"\n{'-'*100}\n")
        print(f"You've succumbed to the terror radiated by {entity.name}.")
        #input("-Press ENTER to end the encounter...")
        return False

  def investigation_encounter(self, player, game):
    #player.use_action()
    print(f"\n{'*'*100}\nInvestigation Encounter: {self.name}\n{'*'*100}\n")
    print("Delve into the abyss where macabre truths and unspeakable horrors intersect.")
    input("\n-Press ENTER to continue...")
    hidden_successes = 0
    hidden_failures = 0
    # Macabre investigative steps replacing the earlier options
    steps_options = {
      'Forensics': [
          "Examine decayed remains for unnatural disturbances.",
          "Investigate the ancient tomes left in a suspicious order.",
          "Analyze the placement of occult symbols covered in dried blood.",
          "Perform spectral analysis to detect ethereal tampering.",
          "Capture electronic voice phenomena with specialized equipment.",
          "Scrutinize old photographs for paranormal distortions."
      ],
      'Séance': [
          "Conduct a forbidden ritual to compel the spirits to reveal their secrets.",
          "Draw a pentagram with ash to form a conduit with the netherworld.",
          "Recite incantations from forgotten texts to pierce the veil between worlds.",
          "Clutch the talisman of banished souls to commune with the dead.",
          "Burn atropa belladonna to slip into a trance and converse with shadows.",
          "Sit in the center of the spirit circle to let the whispers of the damned guide you."
      ],
      'Unnatural Signs': [
          "Inspect the area for eldritch runes and the stain of dark energies.",
          "Seek out places where the fabric of reality frays and thins.",
          "Utilize geomantic tools to trace ley lines corrupted by primordial magicks.",
          "Record discrepancies in time flow with chronometric scanners.",
          "Detect warp signatures emitted by non-Euclidean structures.",
          "Search for marks of the arcane carved by invisible and malevolent entities."
      ]
    }
    for step, options in steps_options.items():
        print(f"\n{'- - '*20}\n")
        print(f"Solve the {step}")
        hidden_values = list(range(1, 7))
        random.shuffle(hidden_values)  # Shuffle hidden values to ensure randomness
        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")
        player_choice = input(f"\n-Choose your methodology for the {step} step (1-{len(options)}): ")
        if player_choice.isdigit() and 1 <= int(player_choice) <= 6:
            chosen_value = hidden_values[int(player_choice) - 1]
            location_mod = player.current_location.investigation_mod
            chosen_value -= location_mod
            roll = chosen_value + player.investigation_value + player.modifiers['investigation'] + player.modifiers['skillroll']
            if roll >= (self.skill_check + random.randint(1,6)):
                hidden_successes += 1

            else:
                hidden_failures += 1
            print(f"\nYour foray into {step} uncovers unsettling findings.")
            input("\n-Press ENTER to proceed into the unknown.")

        else:
            print("Invalid choice, please select a valid number.")
    # Conclusion selection
    print(f"\n{'-'*100}\n")
    print("Gather your thoughts and choose your final hypothesis:")
    hypotheses = ["A sinister force is manipulating events behind the scenes.", "The patterns are too chaotic to be mere coincidence.", "There are still too many shadows clouding the heart of this mystery."]
    while True:
        for idx, hypothesis in enumerate(hypotheses, start=1):
            print(f"{idx}. {hypothesis}")
        hypothesis_choice_str = input("\n-Enter the number of your dark epiphany: ")
        if hypothesis_choice_str.isdigit():
            hypothesis_choice = int(hypothesis_choice_str)
            if 1 <= hypothesis_choice <= 3:
                if hidden_successes > hidden_failures:
                    print(f"\n{'-'*100}\n")
                    print(f"Your relentless investigation has pierced through the enigma of {self.name}.")
                    result = True
                else:
                    print(f"\n{'-'*100}\n")
                    print(f"The inscrutable mystery of {self.name} engulfs your reason in shadow.")
                    #input("-Press ENTER to flee from the encounter...")
                    result = False
                return result
            else:
                print("Invalid choice, please select a number between 1 and 3.")
        else:
            print("Invalid input. Please provide a numerical response.")

  
  def knowledge_encounter(self, player, game):
    #player.use_action()
    entity = Entity("Fiend")
    print(f"\n{'*'*100}\nKnowledge Encounter: {self.name}\n{'*'*100}")
    print(f"\nA wicked enigma presented by the ENTITY {entity}, its eyes aglow with malice, challenges your sanity.")
    challenges = [
        "Cryptic Riddle",
        "Ancient Puzzle",
        "Esoteric Question",
        "Symbolic Interpretation",
        "Logical Conundrum",
        "Philosophical Paradox",
        "Quantum Conundrum",
        "Historical Anomaly",
        "Enigmatic Formula",
        "Scientific Theory Critique",
        "Astronomical Alignment Puzzle",
        "Cryptographic Code Breaking",
        "Philosophical Dilemma",
        "Paranormal Event Analysis",
        "Quantum Mechanic Paradox",
        "Existential Riddle"
    ]
    knowledge_required = random.sample(challenges, self.skill_check)
    rerolls = player.knowledge_value + player.modifiers.get("knowledge", 0)
    location_mod = player.current_location.knowledge_mod
    rerolls -= location_mod
    while knowledge_required:
        challenge = knowledge_required[0]
        #print(f"Challenges ahead: {', '.join(knowledge_required)}")
        print(f"\n{'- - '*20}\n")
        print("Challenges ahead:")
        for idx, challenges in enumerate(knowledge_required):
            #print(f"{idx+1}. {challenges}")
            print(challenges)
        input(f"\nAttempting to solve the challenge: {challenge}.\n\n-Press ENTER to roll the dice...")
        challenge_successful = False
        while not challenge_successful:
            player_roll = self._roll(game,"Player",player)  # Player's d6 roll
            phenomenon_roll = self._roll(game,"Phenomenon",player) # Entity's d6 roll
            if player_roll >= phenomenon_roll:
                print(f"\nChallenge resolved! The insights of the {challenge} have been unraveled.")
                knowledge_required.remove(challenge)
                challenge_successful = True
            else:
                print(f"Attempt failed. Needed at least {phenomenon_roll}, but rolled {player_roll}.")
                rerolls -= 1
                if rerolls < 0:
                    print(f"\n{'-'*100}\n")
                    print(f"No rerolls remaining. The enigmas of {self.name} remain unsolved.")
                    #input("\n-Press ENTER to end the encounter...")
                    return False
                else:
                    input(f"\nAttempting to solve the challenge: {challenge}. You have {rerolls + 1} reroll(s) left.\n-Press ENTER to reroll... ")
    print(f"\n{'-'*100}\n")
    print(f"All challenges have been met. {entity} has been bested!")
    #input("Press ENTER to end the encounter...")
    return True
  
  def stealth_encounter(self, player, game):
    #player.use_action()
    entity = Entity("Beast")
    print(f"\n{'*'*100}\nStealth Encounter: {self.name}\n{'*'*100}")
    print(f"\nThe ENTITY {entity} appears, a creature birthed from nightmares.\nSurvival will require steel nerves and silent footsteps.")
    input("\n-Press ENTER to roll the dice...")
    stealth_messages = {
      'success': [
          "You blend into the shadows, unnoticed by the {entity}.",
          "Your silent steps keep you hidden.",
          "You pause, letting the {entity} pass by, oblivious to your presence.",
          "You use the environment to your advantage, staying out of sight.",
          "The {entity}'s attention is elsewhere, allowing you to slip by."
      ],
      'failure': [
          "You knock over a small object, attracting the {entity}'s gaze.",
          "The {entity} turns suddenly, locking eyes with you.",
          "A misstep causes a loud noise, and the {entity}'s head snaps in your direction.",
          "The {entity} seems to sniff the air and begins moving towards you.",
          "You barely make a sound, but the {entity} somehow senses your presence."
      ]
    }
    roll_sum = 0  
    success = True
    player_mods = player.stealth_value + player.modifiers['stealth']
    location_mods = player.current_location.stealth_mod
    
    for round_number in range(1, self.skill_check + 1):

        player_roll = self._roll(game,"Player",player)# Player's d6 roll
        player_roll -= player_mods
        player_roll += location_mods
        phenomenon_roll = self._roll(game,"Phenomenon",player) # Entity's d6 roll
        
        roll_sum += player_roll
        print(f"\n{'- - '*20}\n")
        print(f"[Round {round_number}/{self.skill_check}]\n")
        print(f"Your roll: {player_roll}")
        print(f"Entity's roll: {phenomenon_roll}")
        #print(f"{entity}'s roll: {entity_roll}")
        if player_roll <= phenomenon_roll:
            message = random.choice(stealth_messages['success']).format(entity=entity)
        else:
            message = random.choice(stealth_messages['failure']).format(entity=entity)
            success = False
        print(f"{message} Roll sum: {roll_sum}")
        input("\n-Press ENTER to continue avoiding the entity...")
    if success and roll_sum <= 0:
        print(f"\n{'-'*100}\n")
        print(f"\n[Success! You've avoided detection by the {entity}.]")
    else:
        print(f"\n{'-'*100}\n")
        print(f"\n[Detected. The {entity} has caught onto your presence.]")
        #input("-Press ENTER to end the encounter...")
        success = False
    #input("Press ENTER to finish the stealth encounter...")
    return success

  def interact(self, player, game):
      resolved = False
      skill_value = f"{self.associated_skill.lower()}_value"
      has_required_item = self.meets_secondary_requirement(player)
      print("\n" + "-" * 50 + "\n")
      print("Phenomenon Active!\n")
      print(self.display())
    # You now need to take into account the location mod for the player's skill level
      player_value = getattr(player, skill_value)
      mod_key = f"{self.associated_skill.lower()}" + "_mod"
      
      #print(mod_key)
      mod_value = 0   
      mod_value += getattr(player.current_location, mod_key)
      #print(mod_value)
      print(f"Your {self.associated_skill} value: {player_value}")

      if player.modifiers['skillroll'] > 0:
          print(f"Your Skill Roll Bonus: {player.modifiers['skillroll']}")
      if mod_value > 0:
          print(f"Location Mod: {mod_value}")
      #    print(f"Total Skill Level: {player_skill_level_with_mod}")
      if has_required_item:
          required_items = [item for item in player.equipment if item.category1 == self.secondary_requirement or item.category2 == self.secondary_requirement]
          print(f"You have {len(required_items)} secondary requirement item(s) of type: {self.secondary_requirement}")
      else:
          print(f"You do not have an item of type: {self.secondary_requirement}")
      print("\nWould you like to try and resolve this phenomenon?")
      print("0. Do not attempt")
      print(f"1. Attempt {self.associated_skill} skill check (Cost: 1 Action)")
      if has_required_item:
        print(f"2. Use a required item of type: {self.secondary_requirement} (Cost: 1 Action)")
      choice = input("\nENTER your choice: ")
      if choice == '1':
          player.use_action()
          encounter_method = getattr(self, f"{self.associated_skill.lower()}_encounter")
          player.attempted_encounter_count += 1
          if encounter_method(player,game):     
              self.resolve(game, player)
          else:
              player.fear += 1
              print(f"You have increased your fear level by 1. Current fear level: {player.fear}") 
              input(f"\n-Press ENTER to continue...")
      elif choice == '2' and has_required_item:
          player.use_action()
          #print("0. Return")
          # Allow the player to choose which item to use if there's more than one
          for idx, item in enumerate(required_items, start=1):
              print("0. Return")
              print(f"{idx}. {item.name}: {item.effect_type} {item.effect_value}")
          item_choice = input(f"Choose which item to use (1-{len(required_items)}): ")
          # Check if the input is valid (a number, and within the range of available items)
          if item_choice.isdigit() and 1 <= int(item_choice) <= len(required_items):
              chosen_item = required_items[int(item_choice) - 1]
              print("\n" + "-" * 50 + "\n")
              print(f"\nYou used {chosen_item.name} to bypass the encounter and resolve the phenomenon!")
              player.equipment.remove(chosen_item)
              self.resolve(game, player)  # Resolve the phenomenon
              player.attempted_encounter_count += 1
          else:
              #print("Invalid selection. Please try again.")
              return
      elif choice == '0':
          #player.current_location.display_location(player,game)
          return
      else:
          print("Invalid selection.")
          self.interact(player,game)
          #return
      
      if resolved and self in player.current_location.phenomena:
          player.cleared_encounter_count += 1
          type_key = f"cleared_{self.effect_desc.lower()}_count"
          setattr(player, type_key, getattr(player, type_key) + 1)
          player.current_location.phenomena.remove(self)
           
  def activate(self, location, player):
    """Activate the phenomenon and apply its effects to the location."""
    if not self.active:
        self.active = True
        # Apply effect to the location's modifiers and store the effect
        effect = location.phenomenon_effect(self, player, 'add')
        if effect:  # If an effect was applied, store it
            self.applied_effects.append(effect)
  
  def resolve(self, game, player):
    """Resolve the phenomenon, reverse its effect, and make it inactive."""
    location = player.current_location
    self.resolved = True
    self.active = False
    player.cleared_encounter_count += 1
    type_key = f"cleared_{self.associated_skill.lower()}_count"
    setattr(player, type_key, getattr(player, type_key) + 1)
    # Reverse effect from the location's modifiers
    location.phenomenon_effect(self, player, 'remove')
    self.applied_effects.clear()  # Clear the effects now that they've been reversed
    print(self.resolution)
    player.current_location.phenomena.remove(self)
    print(f"\nCongratulations, you have resolved the phenomenon: {self.name}")
    input("Press ENTER to collect your rewards!")
    self.grant_reward(player,game)
    #player.use_action()
    input("\nPress ENTER to continue...")

  def _roll(self, game, target, player):
    """Simulate rolling a dice with the value depending on the current moon phase."""
    current_turn = game.turn
    current_phase = game.phase
    d6_value = random.randint(1, 6)
    if target == "Player":
        d6_value += player.modifiers['skillroll']
    # New moon has no effect

    # During the first Half Moon phase, Player's dice is d5
    if current_phase == "Half Moon" and current_turn % 4 == 2 and target == "Player":
        d6_value = random.randint(1, 5)
    # During the second Half Moon phase, Phenomenon's dice is d7
    if current_phase == "Half Moon" and current_turn % 4 == 0 and target == "Phenomenon":
        d6_value = random.randint(1, 7)
    # During Full Moon, apply both Half Moon effects
    if current_phase == "Full Moon" and target == "Player":
        d6_value = random.randint(1,5)
    if current_phase == "Full Moon" and target == "Phenomenon":
        d6_value = random.randint(1,7)
    return d6_value

  def grant_key_reward(self, player):
    """Grants a key to the player as a rare reward."""
    if random.random() < 0.55:  # 5% chance to obtain a key
        player.keys += 1
        print("\nCongratulations, you've obtained a key that can unlock locked doors!")
        key_image = r"""
            _____________
           /      _      \
           [] :: (_) :: []
           [] ::::::::: []
           [] ::::::::: []
           [] ::::::::: []
           [] ::::::::: []
           [_____________]
               I     I
               I_   _I
                /   \
                \   /
                (   )   
                /   \
                \___/
        """
        print(key_image)

  def grant_reward(self,player,game):
    """Grants a reward to the player based on the difficulty of the phenomenon."""
    if self.difficulty == "Common":
      reward_pool = common_items
    elif self.difficulty == "Uncommon":
      reward_pool = common_items + uncommon_items
    elif self.difficulty == "Rare":
      reward_pool = common_items + uncommon_items + rare_items
    
  # Choose and remove the item from its deck
    if reward_pool:
        reward_item = random.choice(reward_pool)
        if reward_item in common_items:
          common_items.remove(reward_item)
        elif reward_item in uncommon_items:
          uncommon_items.remove(reward_item)
        elif reward_item in rare_items:
          rare_items.remove(reward_item)
        player.receive_new_item(reward_item)
        game.item_deck.remove(reward_item)
    else:
      print(f"\nNo {self.difficulty} items left!")

    self.grant_key_reward(player)
    player.gain_experience(self.difficulty,game)
  
  def display(self):
    skill_display = f"Skill Check: {self.skill_check} {self.associated_skill}"
    #if self.effect_value > 0 and self.effect_type = "add":
    return (
        f"Name: {self.name}\n"
        f"Description: {self.description}\n"
        f"Difficulty: {self.difficulty}\n"
        #f"{self.effect_desc} altered by {self.effect_value}\n"
        f"{skill_display}\n"
        #f"Secondary Requirement: {self.secondary_requirement}\n"
        )
    