# from Mob_Generation_fix import Mob
from characterCreation import Character
from console.repository.CharactersDB import CharacterRepository
from models.HealthBar import HealthBar


def pvp_init():
    my_character = Character()
    enemy_character = Character()
    request = {
        'my_character': my_character,
        'enemy_character': enemy_character
    }
    return request

# def generate_start_phrase():
#     character_repository = CharacterRepository
#
# response = str(input('Choose your game mode:'
#                      '\n[1] - PVP'
#                      '\n[2] - PVE\n'))
#
#
#
#
#


response = str(input('Choose your game mode:'
                     '\n[1] - PVP'
                     '\n[2] - PVE\n'))

if response == '1':
    print('Moving to PVP')
    characters = pvp_init()
    my = characters['my_character']
    enemy = characters['enemy_character']
    my_repo = CharacterRepository(my)
    enemy_repo = CharacterRepository(enemy)
    my_bar = HealthBar(max_health=my.health, curr_health=my.health)
    enemy_bar = HealthBar(max_health=enemy.health, curr_health=enemy.health)
    print(f'You: {my}\n'
          f'{my_bar}\n'
          f'Enemy: {enemy}\n'
          f'{enemy_bar}\n')
    response = str(input('Choose your power up:\n'
                         '[1] - +1 hp\n'
                         '[2] - +1 armor\n'))
    if response == '1':
        my.health += 1
        my_bar.curr_health += 1
    elif response == '2':
        my.armor += 1
    my_repo.update_character(my)
    while my.alive and enemy.alive:
        print(f'You: {my}\n'
              f'{my_bar}\n'
              f'Enemy: {enemy}\n'
              f'{enemy_bar}\n')
        response = str(input('Choose your action:'
                             '\n[1] - attack\n'))
        if response == '1':
            enemy.take_damage(my.critical_attack)
            my.take_damage(enemy.critical_attack)
            enemy.reset_luck()
            my.reset_luck()
            my_repo.update_character(my)
            enemy_repo.update_character(enemy)
            my_bar.curr_health = my.health
            enemy_bar.curr_health = enemy.health
    if not enemy.alive:
        print('You win')
    else:
        print('You lose')


elif response == '2':
    print('Moving to PVE')
