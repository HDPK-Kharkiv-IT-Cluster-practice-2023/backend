from flask import Flask, render_template, request, jsonify
import json 

from ConsoleGame import *
from Mappers import *
from characterCreation import Character
from Mob_Generation_fix import Mob
from repository.CharactersDB import CharacterRepository
from repository.MobbDB import MobRepository

# hero = None
# enemy = None
# game_mode = None
character_repository = CharacterRepository()
mob_repository = MobRepository()
app = Flask(__name__, template_folder="templates")

@app.route('/api/v1/status')
def status():
    response = {'status': 'OK'}
    return jsonify(response)

@app.route('/api/v1/characters/<playability>')
def get_characters(playability):
    isPlayable = playability.lower() == 'true'
    response = jsonify(character_repository.find_all_by_playability_and_alive(playability=isPlayable))
    print(character_repository.find_all_by_playability_and_alive(playability=isPlayable))
    response.headers['Content-Type'] = 'application/json'
    return response

# @app.route('/addcharacter', methods=['POST'])
# def generate_hero():
#     generated_hero = Character(playability=True, xp=0)
#     character_repository.add_character(generated_hero)
#     return jsonify({"message": "Character has been created."})
#
# @app.route('/selectcharacter', methods=['POST'])
# def select_character():
#     global hero
#     print(request.form['post'])
#     if request.method == 'POST':
#         if 'post' in request.form:
#             pvp_response = request.form['post']
#             index = int(pvp_response)
#             heroes_list = character_repository.find_all_by_playability_and_alive(playability=True)
#             hero = heroes_list.pop(index)
#             hero = map_dictionary_to_character(hero)
#     return jsonify({"message": "Character has been created."})
#
# @app.route('/selectmode', methods=['POST'])
# def choose_game_mode():
#     global game_mode
#     if request.method == 'POST':
#         if 'post' in request.form:
#             response = request.form['post']
#             if response == '1':
#                 game_mode = 1
#                 print('Moving to PVP\n')
#             elif response == '2':
#                 game_mode = 2
#                 print('Moving to PVE\n')
#     return jsonify({"message": "Game mode has been selected."})
#
# @app.route('/selectenemy', methods=['POST'])
# def select_enemy():
#     global enemy
#     global enemies_list
#     print(request.form['post'])
#     if request.method == 'POST':
#         enemies_list = character_repository.find_all_by_playability_and_alive_and_level(level=hero.level,
#                                                                                         playability=False)
#         enemy = enemies_list.pop(random.randint(0, len(enemies_list) - 1))
#         enemy = map_dictionary_to_character(enemy)
#         print(enemy)
#     return jsonify({"message": "Character has been created."})
#
# @app.route('/addenemy', methods=['POST'])
# def generate_enemy():
#     new_enemy = Character(playability=False, level=random.randint(hero.level - 1, hero.level + 1))
#     character_repository.add_character(new_enemy)
#     return jsonify({"message": "Character has been created."})
#
# @app.route('/character')
# def c():
#     jsoncharacter = hero.toJSON()
#     response = jsonify(jsoncharacter)
#     response.headers['Content-Type'] = 'application/json'
#     return response.json
#
# @app.route('/enemy')
# def e():
#     jsonenemy = enemy.toJSON()
#     response = jsonify(jsonenemy)
#     response.headers['Content-Type'] = 'application/json'
#     return response.json
# @app.route('/character2')
# def c2():
#     jsoncharacter2 = json.dumps(character2.__dict__)
#     response = jsonify(jsoncharacter2)
#     response.headers['Content-Type'] = 'application/json'
#     return response.json

# @app.route('/mob')
# def m():
#     jsonmob = json.dumps(mob1.__dict__)
#     response = jsonify(jsonmob)
#     response.headers['Content-Type'] = 'application/json'
#     return response.json

# @app.route('/', methods=['GET', 'POST'])
# def start():
#     return render_template('start.html')

# @app.route('/fight_mob', methods=['GET', 'POST'])
# def fight_mob():
#     if mob1.health <= 0:
#         character1.xp += mob1.xp
#         character1.balance += 25
#         mob1.__init__()
#     mob1.take_damage(character1.critical_attack)
#     character1.take_damage(mob1.critical_attack)
#     character1.reset_attack()
#     character1.reset_luck()

#     if character1.xp >= 100:
#         character1.level += 1
#         character1.xp -= 100

#     if character1.health <= 0:
#         return render_template('game_over.html')

#     return render_template('fight_mob.html', character=character1, mob=mob1)


# @app.route('/fight_character', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'c1damage' in request.form:
#             if request.form['c1damage'] == 'damage':
#                 character1.take_damage(character2.critical_attack)
#                 character2.take_damage(character1.critical_attack)
#                 character1.reset_attack()
#                 character2.reset_attack()
#                 character1.reset_luck()
#                 character2.reset_luck()

#         if character1.health <= 0:
#             character1.alive = False
#             return render_template('winner.html', character=character2)
#         if character2.health <= 0:
#             character1.alive = False
#             return render_template('winner.html', character=character1)

#     return render_template('fight_character.html', character1=character1, character2=character2,)


@app.route('/api/v1/mobs')
def get_mobs():
    response = jsonify(mob_repository.find_all_by_alive())
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/v1/mob/<mob_id>')
def get_mob_by_id(mob_id):
    mob = mob_repository.find_by_id(mob_id)
    if mob is None:
        return jsonify({"message": f"There's no mob with an id {mob_id}"}), 404
    return jsonify({'mob': mob})


@app.route('/api/v1/mob/<character_id>', methods=['POST'])
def add_mob(character_id):
    character = character_repository.find_by_id(character_id)
    if character is None:
        return jsonify({"message": f"There's no character with an id {character_id}"}), 404
    else:
        character = map_dictionary_to_character(character)
        mob_id = mob_repository.add_mob(Mob(character))
        return jsonify({"mob_id": f'{mob_id}'})


@app.route('/api/v1/fight/<hero_id>/<enemy_id>')
def start_fight(hero_id, enemy_id):
    hero = character_repository.find_by_id(hero_id)
    if hero is None:
        return jsonify({"message": f"There's no hero with an id {hero_id}"}), 404
    hero = map_dictionary_to_character(hero)
    enemy_type = request.args.get('enemy_type')
    if enemy_type == 'mob':
        enemy = mob_repository.find_by_id(enemy_id)
    elif enemy_type == 'character':
        enemy = character_repository.find_by_id(enemy_id)
    else:
        return jsonify({'error': 'cannot find parameter enemy_type'}), 404
    if enemy is None:
        return jsonify({"message": f"There's no enemy with an id {enemy_id}"}), 404
    enemy = map_dictionary_to_mob(enemy)
    action = request.args.get('action')
    message = ''
    if action == 'attack':
        enemy.take_damage(hero)
        hero.take_damage(enemy)
        update_characters_info(hero, enemy, True)
    elif action == 'escape':
        if hero.dice.roll_dice() <= hero.luck:
            message = 'You successfully escaped'
            update_characters_info(hero, enemy)
        else:
            message = 'You couldn\'t escape'
            enemy_curr_luck = enemy.luck
            enemy.luck = 100
            hero.take_damage(enemy)
            enemy.luck = enemy_curr_luck
            update_characters_info(hero)
            update_characters_info(enemy=enemy, update_bars=True)
    hero = map_character_to_dictionary(hero)
    enemy = map_mob_to_dictionary(enemy)
    response = {'hero': hero,
                'enemy': enemy,
                'message': message}
    return jsonify(response)


@app.route('/api/v1/character/<character_id>', methods=['PATCH'])
def update_character(character_id):
    character = character_repository.find_by_id(character_id)
    if character is None:
        return jsonify({"message": f"There's no character with an id {character_id}"}), 404
    else:
        data = request.get_json()
        for key, value in data.items():
            character[key] = value
        character_repository.update_character(map_dictionary_to_character(character))
        return jsonify({'character': character})


@app.route('/api/v1/character', methods=['POST'])
def create_character():
    data = request.get_json()
    character = map_dictionary_to_character(data)
    character_id = character_repository.add_character(character)
    return jsonify({'character_id': character_id})


if __name__ == "__main__":
    app.run(debug=True)
