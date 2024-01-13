import random
import json

with open('entity_dictionary.json', 'r') as file:
    data = json.load(file)

class Entity:

    def __init__(self,race):
        self.race = race
        self.name = self.generate_name()
        
    def generate_name(self):
        """Generate a random name based on race."""
        race = self.race
        cardName = ""
        cardType = ""
        if race == "Dragon":
            cardName += random.choice(data['dragonName'])
            for _ in range(random.randint(2, 4)):
                cardName += random.choice(data['dragonName2'])
            cardName += random.choice(data['dragonName'])
            cardType = random.choice(data['dragonMod']) + " " + random.choice(data['dragonType'])

        elif race == "Beast":
            cardName += "The " + random.choice(data['beastMod']) + " "
            for _ in range(random.randint(3, 4)):
                cardName += random.choice(data['beastName'])
            cardType = random.choice(data['beastType'])

        elif race == "Zombie":
            for _ in range(random.randint(2, 5)):
                cardName += random.choice(data['zombieName'])
            cardType = random.choice(data['zombieMod']) + " " + random.choice(data['zombieType'])

        elif race == "Fiend":
            for _ in range(random.randint(2, 4)):
                cardName += random.choice(data['fiendName'])
            cardName += " The " + random.choice(data['fiendMod'])
            cardType = random.choice(data['fiendType'])

        elif race == "Phantom":
            for _ in range(random.randint(2, 3)):
                cardName += random.choice(data['phantomName'])
            cardName += " Of The " + random.choice(data['phantomMod'])
            cardType = random.choice(data['phantomType'])

        elif race == "Arcane":
            for _ in range(random.randint(2, 4)):
                cardName += random.choice(data['arcaneName'])
            cardType += random.choice(data['arcaneMod']) + " " + random.choice(data['arcaneType'])

        elif race == "Human":
            cardName = random.choice(data['humanName']) + " " + random.choice(data['humanName2'])
            cardType = random.choice(data['humanMod']) + " " + random.choice(data['humanType'])
        
        entity_name = f"{cardName.title()} - {cardType}"
        return entity_name

    def __str__(self):
        return self.name
