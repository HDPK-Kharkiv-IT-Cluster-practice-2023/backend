import random
from characters import Character
# game_logic.py

character1 = Character("Кирило")
character2 = Character("Жэня")


def damageDeterminator():
    global damagePlayer1
    damagePlayer1 = random.randint(1, character1.attack) + character1.critical_attack
    global damagePlayer2
    damagePlayer2 = random.randint(1, character2.attack) + character2.critical_attack
    return damagePlayer1, damagePlayer2


def player_turn(character1, character2):
    while True:
        action = input(f"{character1.name}, оберіть дію (атака/ухил/стата): ").lower()
        if action == "атака":
            return damagePlayer1
        elif action == "ухил":
            dodge_damage = damagePlayer2 - 5  # Dodging causes less damage
            print(f"{character1.name} ухиляється від атаки {character2.name} ({damagePlayer2} ушкодження) і отримує {dodge_damage} ушкодження")
            return -dodge_damage  # Negative value to indicate dodging
        elif action == "стата":
            print(f"{character1}\n{character2}")
        else:
            print("Некоректна дія. Будь ласка, оберіть атакувати, ухилятися або стати.")


def enemy_turn(character1, character2):
   
    # Enemy decides to attack or dodge
    action = random.choice(["атакувати", "ухилятися"])
    if action == "атакувати":
        damagePlayer2
        return damagePlayer2
    else:
        dodge_damage = damagePlayer1 - 5  # Dodging causes less damage
        print(f"{character2.name} ухиляється від атаки {character1.name} ({damagePlayer1} ушкодження) і отримує {dodge_damage} ушкодження")
        return -dodge_damage  # Negative value to indicate dodging


def fight(character1, character2):
    round_number = 1
    while character1.health > 0 and character2.health > 0:
        print(f"Раунд {round_number}:")
        
        # Player's turn
        player_damage = player_turn(character1, character2)
        if player_damage > 0:
            character2.take_damage(player_damage)
            print(f"{character1.name} атакує {character2.name} та наносить {player_damage} ушкодження")
        elif player_damage < 0:
            # Output dodge damage
            pass  # Already printed in player_turn

        # Check if Character 2 is still alive
        if character2.health <= 0:
            print(f"{character2.name} переможений!")
            break

        # Enemy's turn
        enemy_damage = enemy_turn(character1, character2)
        if enemy_damage > 0:
            character1.take_damage(enemy_damage)
            print(f"{character2.name} атакує {character1.name} та наносить {enemy_damage} ушкодження")
        elif enemy_damage < 0:
            # Output dodge damage
            pass  # Already printed in enemy_turn

        # Check if Character 1 is still alive
        if character1.health <= 0:
            print(f"{character1.name} побежден!")

        round_number += 1