# main.py
import random
from characters import Character
from game_logic import fight, character1, character2, damageDeterminator

damageDeterminator()

# Start the game
fight(character1, character2)
