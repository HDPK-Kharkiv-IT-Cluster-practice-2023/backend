from flask import Flask, render_template, request, jsonify

from ConsoleGame import *
from characterCreation import Character
from Mob_Generation_fix import Mob
from repository.CharactersDB import CharacterRepository
from repository.MobbDB import MobRepository

import json

hero = None
enemy = None
game_mode = None
character_repository = CharacterRepository()
app = Flask(__name__, template_folder="templates")


# @app.route('/init', methods=['POST'])
# def restart():
#     character1.__init__()
#     character2.__init__()
#     return jsonify({"message": "Characters have been restarted."})

@app.route('/characterslist')
def cl():
    jsoncharacter1 = json.dumps(character_repository.find_all_by_playability_and_alive(playability=True))
    response = jsonify(jsoncharacter1)
    response.headers['Content-Type'] = 'application/json'
    print(hero)
    return response.json

@app.route('/addcharacter', methods=['POST'])
def generate_hero():
    generated_hero = Character(playability=True, xp=0)
    character_repository.add_character(generated_hero)
    return jsonify({"message": "Character has been created."})

@app.route('/selectcharacter', methods=['POST'])
def select_character():
    global hero
    global heromapped
    print(request.form['post'])
    if request.method == 'POST':
        if 'post' in request.form:
            pvp_response = request.form['post']
            index = int(pvp_response)
            heroes_list = character_repository.find_all_by_playability_and_alive(playability=True)
            hero = heroes_list.pop(index)
            hero = map_dictionary_to_character(hero)
    return jsonify({"message": "Character has been created."})

@app.route('/selectmode', methods=['POST'])
def choose_game_mode():
    global game_mode
    if request.method == 'POST':
        if 'post' in request.form:
            response = request.form['post']
            if response == '1':
                game_mode = 1
                print('Moving to PVP\n')
            elif response == '2':
                game_mode = 2
                print('Moving to PVE\n')
    return jsonify({"message": "Game mode has been selected."})

@app.route('/enemylist')
def el():
    enemylist = json.dumps(character_repository.find_all_by_playability_and_alive_and_level(level=hero.level,
                                                                                        playability=False))
    response = jsonify(enemylist)
    response.headers['Content-Type'] = 'application/json'
    print(enemy)
    return response.json

@app.route('/selectenemy', methods=['POST'])
def select_enemy():
    global enemy
    print(request.form['post'])
    if request.method == 'POST':
        enemies_list = character_repository.find_all_by_playability_and_alive_and_level(level=hero.level,
                                                                                        playability=False)
        enemy = enemies_list.pop(random.randint(0, len(enemies_list) - 1))
    return jsonify({"message": "Character has been created."})

@app.route('/character')
def c():
    jsoncharacter = json.dumps(hero)
    response = jsonify(jsoncharacter)
    response.headers['Content-Type'] = 'application/json'
    return response.json

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


if __name__ == "__main__":
    app.run(debug=True)
