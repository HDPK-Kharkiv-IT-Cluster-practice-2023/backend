# from Mob_Generation_fix import Mob
import random

from console.characterCreation import Character
from console.repository.CharactersDB import CharacterRepository
from models.HealthBar import HealthBar

character_repository = CharacterRepository()


# def pvp_characters_init():
#     my_character = Character(playability=True)
#     enemy_character = Character()
#     request = {
#         'my_character': my_character,
#         'enemy_character': enemy_character
#     }
#     return request


def generate_hero():
    generated_hero = Character(playability=True)
    character_repository.add_character(generated_hero)
    return generated_hero


def generate_enemies(count):
    counter = 0
    enemies_list = []
    while counter < count:
        enemies_list.append(Character(playability=False))
        counter += 1
    character_repository.add_all(enemies_list)
    return enemies_list


def generate_character_chooser(characters_list):
    request = 'Choose your character\n'
    i = 1
    for character in characters_list:
        request += (f'[{i}] - [Name: {character.get("name")}, '
                    f'Crit: {character.get("critical_attack")}, '
                    f'Health: {character.get("health")}, '
                    f'Armor: {character.get("armor")}, '
                    f'Attack: {character.get("attack")}, '
                    f'Luck: {character.get("luck")}]\n')
        i += 1
    return request


def map_dictionary_to_character(character):
    return Character(name=character.get("name"), level=character.get("level"), xp=character.get("xp"),
                     max_health=character.get("max_health"), health=character.get("health"),
                     armor=character.get("armor"), attack=character.get("attack"), luck=character.get("luck"),
                     balance=character.get("balance"), alive=character.get("alive"),
                     critical_attack=character.get("critical_attack"), playability=character.get("playability"))


def pvp_init():
    heroes_list = character_repository.find_all_by_playability_and_alive(playability=True)
    hero = None
    if not heroes_list:
        pvp_response = str(input('You don\'t have characters yet, want to create one?\n'
                                 '[1] - Yes\n'
                                 '[2] - No\n\n'))
        if pvp_response == '1':
            hero = generate_hero()
        elif pvp_response == '2':
            start_game()
    else:
        print(generate_character_chooser(heroes_list))
        while True:
            pvp_response = str(input())
            try:
                index = int(pvp_response)
                hero = heroes_list.pop(index - 1)
                hero = map_dictionary_to_character(hero)
                break
            except (ValueError, IndexError):
                print('Invalid entry, enter a number from the list above')
    enemies_list = character_repository.find_all_by_playability_and_alive(playability=False)
    if not enemies_list:
        print('Looks like you don\'t have any enemies, how many do you want to create '
              '(write the number)\n')
        while True:
            pvp_response = str(input())
            try:
                count = int(pvp_response)
                break
            except ValueError:
                print('Invalid entry, enter a number from the list above')
        enemies_list = generate_enemies(count)
        enemy = enemies_list.pop(random.randint(0, len(enemies_list) - 1))
    else:
        enemy = enemies_list.pop(random.randint(0, len(enemies_list) - 1))
        enemy = map_dictionary_to_character(enemy)
    return {
        'my_character': hero,
        'enemy_character': enemy
    }


def display_pvp_status(first, first_bar, second, second_bar):
    return (f'You: {first.name}\n'
            f'{first_bar}\n'
            f'Crit: {first.critical_attack}, '
            f'Health: {first.health}, '
            f'Armor: {first.armor}, '
            f'Attack: {first.attack}, '
            f'Luck: {first.luck}\n'
            f'Enemy: {second.name}\n'
            f'{second_bar}\n'
            f'Crit: {second.critical_attack}, '
            f'Health: {second.health}, '
            f'Armor: {second.armor}, '
            f'Attack: {second.attack}, '
            f'Luck: {second.luck}\n')


def start_game():
    response = str(input('Choose your game mode:\n'
                         '[1] - PVP\n'
                         '[2] - PVE\n\n'))
    if response == '1':
        print('Moving to PVP')
        characters = pvp_init()

        hero = characters.get('my_character')
        my_bar = HealthBar(max_health=hero.max_health, curr_health=hero.health)

        enemy = characters.get('enemy_character')
        enemy_bar = HealthBar(max_health=enemy.max_health, curr_health=enemy.health)

        print(display_pvp_status(hero, my_bar, enemy, enemy_bar))
        response = str(input('Choose your power up:\n'
                             '[1] - +15 hp\n'
                             '[2] - +1 armor\n\n'))
        if response == '1':
            hero.health += 15
            my_bar.update_health(hero.health)
        elif response == '2':
            hero.armor += 1
        character_repository.update_character(hero)

        while hero.alive and enemy.alive:
            print(display_pvp_status(hero, my_bar, enemy, enemy_bar))
            response = str(input('Choose your action:\n'
                                 '[1] - attack\n\n'))
            if response == '1':
                enemy.take_damage(hero)
                hero.take_damage(enemy)
                character_repository.update_character(hero)
                character_repository.update_character(enemy)
                my_bar.update_health(hero.health)
                enemy_bar.update_health(enemy.health)
        print(display_pvp_status(hero, my_bar, enemy, enemy_bar))
        if not enemy.alive:
            print('You win')
        else:
            print('You lose')

    elif response == '2':
        print('Moving to PVE')


if __name__ == "__main__":
    start_game()
