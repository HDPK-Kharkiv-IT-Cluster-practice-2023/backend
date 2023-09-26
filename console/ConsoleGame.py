# from Mob_Generation_fix import Mob
import random

from console.characterCreation import Character
from console.repository.CharactersDB import CharacterRepository

character_repository = CharacterRepository()


def generate_hero():
    generated_hero = Character(playability=True, xp=0)
    character_repository.add_character(generated_hero)
    return generated_hero


def generate_enemies(count, character):
    counter = 0
    enemies_list = []
    while counter < count:
        enemies_list.append(Character(playability=False,
                                      level=random.randint(character.level - 1, character.level + 1)))
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
    return Character(id=character.get('id'), name=character.get("name"), level=character.get("level"),
                     xp=character.get("xp"), max_health=character.get("max_health"), health=character.get("health"),
                     armor=character.get("armor"), attack=character.get("attack"), luck=character.get("luck"),
                     balance=character.get("balance"), alive=character.get("alive"),
                     critical_attack=character.get("critical_attack"), playability=character.get("playability"))


def select_hero():
    heroes_list = character_repository.find_all_by_playability_and_alive(playability=True)
    if not heroes_list:
        pvp_response = str(input('You don\'t have characters yet, want to create one?\n'
                                 '[1] - Yes\n'
                                 '[2] - No\n\n'))
        if pvp_response == '1':
            return generate_hero()
        elif pvp_response == '2':
            start_game()
    else:
        print(generate_character_chooser(heroes_list))
        while True:
            pvp_response = str(input())
            try:
                index = int(pvp_response)
                hero = heroes_list.pop(index - 1)
                break
            except (ValueError, IndexError):
                print('Invalid entry, enter a number from the list above')
        return map_dictionary_to_character(hero)


def select_enemy(character):
    enemies_list = character_repository.find_all_by_playability_and_alive_and_level(level=character.level,
                                                                                    playability=False)
    if not enemies_list:
        print('Looks like you don\'t have any enemies, how many do you want to create? '
              '(write the number)\n')
        while True:
            pvp_response = str(input())
            try:
                count = int(pvp_response)
                break
            except ValueError:
                print('Invalid entry, enter a number from the list above')
        enemies_list = generate_enemies(count, character)
        return enemies_list.pop(random.randint(0, len(enemies_list) - 1))
    else:
        enemy = enemies_list.pop(random.randint(0, len(enemies_list) - 1))
        return map_dictionary_to_character(enemy)


def apply_power_up(character):
    input_prompt = 'Choose your power up:\n'
    first_power_up = generate_power_up(character)
    second_power_up = generate_power_up(character)
    input_prompt += f'[1] - +{first_power_up[1]} {first_power_up[0]}\n'
    input_prompt += f'[2] - +{second_power_up[1]} {second_power_up[0]}\n\n'
    print(input_prompt)
    while True:
        response = str(input())
        if response == '1':
            buff = first_power_up
            break
        elif response == '2':
            buff = second_power_up
            break
        else:
            print('Invalid entry, enter a number from the list above')
    if buff[0] == 'health':
        character.health += buff[1]
    elif buff[0] == 'attack':
        character.attack += buff[1]
    elif buff[0] == 'armor':
        character.armor += buff[1]


def generate_power_up(character):
    power_up_variants = ['health', 'attack', 'armor']
    power_up = random.choice(power_up_variants)
    if power_up == 'health':
        health = random.randint(character.max_health // 4, character.max_health // 2)
        return ['health', health]
    elif power_up == 'attack':
        attack = random.randint(1, 5)
        return ['attack', attack]
    elif power_up == 'armor':
        armor = random.randint(1, 5)
        return ['armor', armor]


def update_characters_info(hero, enemy):
    character_repository.update_character(hero)
    character_repository.update_character(enemy)


def pvp_fight(hero, enemy):
    while hero.alive and enemy.alive:
        print(str(hero) + '\n' + str(enemy))
        if hero.dice.roll_dice() <= hero.luck:
            apply_power_up(hero)
            update_characters_info(hero, enemy)
            hero.update_bars()
            enemy.update_bars()
            print(str(hero) + '\n' + str(enemy))
        response = str(input('Choose your action:\n'
                             '[1] - attack\n'
                             '[2] - run away\n\n'))
        if response == '1':
            enemy.take_damage(hero)
            hero.take_damage(enemy)
            update_characters_info(hero, enemy)
        elif response == '2':
            if hero.dice.roll_dice() <= hero.luck:
                print('You successfully escaped\n')
                update_characters_info(hero, enemy)
                hero.update_bars()
                enemy.update_bars()
                break
            else:
                print('You couldn\'t escape\n')
                enemy_curr_luck = enemy.luck
                enemy.luck = 100
                hero.take_damage(enemy)
                enemy.luck = enemy_curr_luck
                update_characters_info(hero, enemy)
                enemy.update_bars()
    print(str(hero) + '\n' + str(enemy))


def start_game():
    response = str(input('Choose your game mode:\n'
                         '[1] - PVP\n'
                         '[2] - PVE\n\n'))
    if response == '1':
        print('Moving to PVP\n')
        hero = select_hero()
        start_pvp(hero)
    elif response == '2':
        print('Moving to PVE\n')


def start_pvp(hero):
    enemy = select_enemy(hero)
    pvp_fight(hero, enemy)
    if hero.alive:
        if not enemy.alive:
            print('You win\n')
        response = str(input('Continue?\n'
                             '[1] - Yes\n'
                             '[2] - No\n\n'))
        if response == '1':
            start_pvp(hero)
        elif response == '2':
            start_game()
    else:
        print('Game over\n')
        start_game()


if __name__ == "__main__":
    start_game()
