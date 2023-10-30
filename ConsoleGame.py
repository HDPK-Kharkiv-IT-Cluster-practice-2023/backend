import random
import sys

from repository.characters_db import CharacterRepository
from repository.mobb_db import MobRepository
from mappers import *

character_repository = CharacterRepository()
mob_repository = MobRepository()


def crate_hero_manually():
    print('Write the following characteristics across the space:\n'
          'level max_health armor attack luck\n')
    while True:
        response = str(input())
        response_values = response.split()
        if len(response_values) != 5:
            print('Invalid entry, enter 5 numbers across the space')
            continue
        try:
            values = [int(i) for i in response_values]
        except ValueError:
            print('Invalid entry, enter only numbers')
            continue
        try:
            generated_hero = Character(level=values[0], max_health=values[1], armor=values[2], attack=values[3],
                                       luck=values[4], playability=True, xp=0)
            character_repository.add_character(generated_hero)
            print(generated_hero)
            return generated_hero
        except OverflowError:
            print(f'Invalid entry, for level {values[0]} max number of stat points is '
                  f'{Character.calculate_stat_points_by_level(values[0])}')


def crate_hero_random():
    generated_hero = Character(playability=True, xp=0)
    print(f'Your hero: \n{generated_hero}\n')
    response = str(input('Do you want to create that character?\n'
                         '[1] - Yes\n'
                         '[2] - No\n\n'))
    if response == '1':
        character_repository.add_character(generated_hero)
        return generated_hero
    else:
        return crate_hero_random()


def generate_hero():
    response = str(input('Choose generation type: \n'
                         '[1] - Manually\n'
                         '[2] - Random\n\n'))
    if response == '1':
        return crate_hero_manually()
    elif response == '2':
        return crate_hero_random()


def generate_enemies(count, character, is_mob):
    counter = 0
    enemies_list = []
    while counter < count:
        if is_mob:
            enemies_list.append(Mob(character))
        else:
            if character.level - 1 == 0:
                min = 1
            else:
                min = character.level - 1
            max = character.level + 1
            enemies_list.append(Character(playability=False,
                                          level=random.randint(min, max)))
        counter += 1
    if is_mob:
        mob_repository.add_all(enemies_list)
    else:
        character_repository.add_all(enemies_list)
    return enemies_list


def generate_character_chooser(characters_list):
    request = 'Choose your character\n'
    i = 1
    for character in characters_list:
        request += (f'[{i}] - [{character.get("name")}, '
                    f'Health: {character.get("health")}/{character.get("max_health")}, '
                    f'Level: {character.get("level")}, '
                    f'Attack: {character.get("attack")}, '
                    f'Armor: {character.get("armor")}, '
                    f'Luck: {character.get("luck")}, '
                    f'Crit: {character.get("critical_attack")}, '
                    f'Balance: {character.get("balance")}, '
                    f'Points: {character.get("stat_points")}]\n')
        i += 1
    request += f'[{i}] - Generate new character\n'
    return request


def select_hero():
    heroes_list = character_repository.find_all_by_playability_and_alive(playability=True)
    if not heroes_list:
        pvp_response = str(input('You don\'t have characters yet, want to create one?\n'
                                 '[1] - Yes\n'
                                 '[2] - No\n\n'))
        if pvp_response == '1':
            return generate_hero()
        elif pvp_response == '2':
            sys.exit()
    else:
        print(generate_character_chooser(heroes_list))
        while True:
            pvp_response = str(input())
            try:
                index = int(pvp_response)
                if index == len(heroes_list) + 1:
                    generate_hero()
                    return select_hero()
                hero = heroes_list.pop(index - 1)
                break
            except (ValueError, IndexError):
                print('Invalid entry, enter a number from the list above')
        return map_dictionary_to_character(hero)


def select_enemy(character, is_mob=False):
    if is_mob:
        enemies_list = mob_repository.find_all_by_alive_and_level(level=character.level)
    else:
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
        enemies_list = generate_enemies(count, character, is_mob)
        return enemies_list.pop(random.randint(0, len(enemies_list) - 1))
    else:
        enemy = enemies_list.pop(random.randint(0, len(enemies_list) - 1))
        if is_mob:
            return map_dictionary_to_mob(enemy)
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


def update_characters_info(hero=None, enemy=None, update_bars=False):
    if hero is not None:
        character_repository.update_character(hero)
        if update_bars:
            hero.update_bars()
    if enemy is not None:
        if isinstance(enemy, Character):
            character_repository.update_character(enemy)
        elif isinstance(enemy, Mob):
            mob_repository.update_mob(enemy)
        if update_bars:
            enemy.update_bars()


def pvp_fight(hero, enemy):
    while hero.alive and enemy.alive:
        print(str(hero) + '\n' + str(enemy))
        if hero.dice.roll_dice() <= hero.luck:
            apply_power_up(hero)
            update_characters_info(hero, enemy, True)
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
                update_characters_info(hero, enemy, True)
                break
            else:
                print('You couldn\'t escape\n')
                enemy_curr_luck = enemy.luck
                enemy.luck = 100
                hero.take_damage(enemy)
                enemy.luck = enemy_curr_luck
                update_characters_info(hero)
                update_characters_info(enemy=enemy, update_bars=True)
    print(str(hero) + '\n' + str(enemy))


def choose_game_mode(hero):
    response = str(input('Choose your game mode:\n'
                         '[1] - PVP\n'
                         '[2] - PVE\n'
                         '[3] - Upgrade room\n\n'))
    if response == '1':
        print('Moving to PVP\n')
        start_pvp(hero)
    elif response == '2':
        print('Moving to PVE\n')
        start_pve(hero)
    elif response == '3':
        print('Upgrade room\n')
        upgrade_room(hero)


def start_game():
    hero = select_hero()
    choose_game_mode(hero)


def upgrade_room(hero):
    print(f'You: {hero}')
    print('Write the following characteristics across the space:\n'
          'max_health attack armor luck\n')
    while True:
        response = str(input())
        response_values = response.split()
        if len(response_values) != 4:
            print('Invalid entry, enter 4 numbers across the space')
            continue
        try:
            values = [int(i) for i in response_values]
        except ValueError:
            print('Invalid entry, enter only numbers')
            continue
        try:
            if values[0] < hero.max_health:
                raise ValueError
            if values[1] < hero.attack:
                raise ValueError
            if values[2] < hero.armor:
                raise ValueError
            if values[3] < hero.luck:
                raise ValueError
            hero.skills_up(new_max_health=values[0], new_attack=values[1], new_armor=values[2], new_luck=values[3])
            print(hero)
            break
        except OverflowError:
            print(f'Invalid entry, for level {hero.level} max number of stat points is '
                  f'{hero.calculate_stat_points_by_level(hero.level)}')
        except ValueError:
            print(f'Invalid entry, new stat can\'t be lower than old')

    character_repository.update_character(hero)
    choose_game_mode(hero)


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
            choose_game_mode(hero)
    else:
        print('Game over\n')
        start_game()


def start_pve(hero):
    enemy = select_enemy(hero, is_mob=True)
    pvp_fight(hero, enemy)
    if hero.alive:
        if not enemy.alive:
            print('You win\n')
        response = str(input('Continue?\n'
                             '[1] - Yes\n'
                             '[2] - No\n\n'))
        if response == '1':
            start_pve(hero)
        elif response == '2':
            choose_game_mode(hero)
    else:
        print('Game over\n')
        start_game()


if __name__ == "__main__":
    start_game()
