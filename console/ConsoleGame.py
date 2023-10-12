import random
import sys

from characterCreation import Character
from Mob_Generation_fix import Mob
from repository.CharactersDB import CharacterRepository
from repository.MobbDB import MobRepository

character_repository = CharacterRepository()
mob_repository = MobRepository()


def generate_hero():
    generated_hero = Character(playability=True, xp=0)
    character_repository.add_character(generated_hero)
    return generated_hero


def generate_enemies(count, character, is_mob):
    counter = 0
    enemies_list = []
    while counter < count:
        if is_mob:
            enemies_list.append(Mob(character))
        else:
            enemies_list.append(Character(playability=False,
                                          level=random.randint(character.level - 1, character.level + 1)))
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
                    f'Balance: {character.get("balance")}]\n')
        i += 1
    request += f'[{i}] - Generate new character\n'
    return request


def map_dictionary_to_character(character):
    return Character(id=character.get('id'), name=character.get("name"), level=character.get("level"),
                     xp=character.get("xp"), max_health=character.get("max_health"), health=character.get("health"),
                     armor=character.get("armor"), attack=character.get("attack"), luck=character.get("luck"),
                     balance=character.get("balance"), alive=character.get("alive"),
                     critical_attack=character.get("critical_attack"), playability=character.get("playability"))


def map_dictionary_to_mob(character):
    return Mob(id=character.get('id'), name=character.get("mob_name"), level=character.get("level"),
               xp=character.get("xp"), max_health=character.get("max_health"), health=character.get("health"),
               armor=character.get("armor"), attack=character.get("attack"), luck=character.get("luck"),
               balance=character.get("balance"), alive=character.get("alive"),
               critical_attack=character.get("critical_attack"))


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
                         '[2] - PVE\n\n'))
    if response == '1':
        print('Moving to PVP\n')
        start_pvp(hero)
    elif response == '2':
        print('Moving to PVE\n')
        start_pve(hero)


def start_game():
    hero = select_hero()
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
