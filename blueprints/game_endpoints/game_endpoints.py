from flask import Blueprint
from flask import request, jsonify, make_response, Response

from mappers import *
from ConsoleGame import *


character_repository = CharacterRepository()
mob_repository = MobRepository()
blueprint = Blueprint('game', __name__)


@blueprint.route('/api/v1/status')
def status():
    response = {'status': 'OK'}
    return jsonify(response)


@blueprint.route('/api/v1/characters/<playability>')
def get_characters(playability):
    is_playable = playability.lower() == 'true'
    response = jsonify(character_repository.find_all_by_playability_and_alive(playability=is_playable))
    print(character_repository.find_all_by_playability_and_alive(playability=is_playable))
    response.headers['Content-Type'] = 'application/json'
    return response


@blueprint.route('/api/v1/character/<character_id>')
def get_character_by_id(character_id):
    character = character_repository.find_by_id(character_id)
    if character is None:
        return jsonify({'error': f"There's no mob with an id {character_id}"}), 404
    return jsonify({'character': character})


@blueprint.route('/api/v1/mobs')
def get_mobs():
    response = jsonify(mob_repository.find_all_by_alive())
    response.headers['Content-Type'] = 'application/json'
    return response


@blueprint.route('/api/v1/mob/<mob_id>')
def get_mob_by_id(mob_id):
    mob = mob_repository.find_by_id(mob_id)
    if mob is None:
        return jsonify({'error': f"There's no mob with an id {mob_id}"}), 404
    return jsonify({'mob': mob})


@blueprint.route('/api/v1/mob/<character_id>', methods=['POST'])
def add_mob(character_id):
    character = character_repository.find_by_id(character_id)
    if character is None:
        return jsonify({'error': f"There's no character with an id {character_id}"}), 404
    else:
        character = map_dictionary_to_character(character)
        mob_id = mob_repository.add_mob(Mob(character))
        return jsonify({'mob_id': f'{mob_id}'})


@blueprint.route('/api/v1/fight/<hero_id>/<enemy_id>')
def fight(hero_id, enemy_id):
    hero = character_repository.find_by_id(hero_id)
    if hero is None:
        return jsonify({'error': f"There's no hero with an id {hero_id}"}), 404
    hero = validate_entity(hero)
    if isinstance(hero, Response):
        return hero
    enemy_type = request.args.get('enemy_type')
    if enemy_type == 'mob':
        enemy = mob_repository.find_by_id(enemy_id)
        if enemy is None:
            return jsonify({'error': f"There's no enemy with an id {enemy_id}"}), 404
    elif enemy_type == 'character':
        enemy = character_repository.find_by_id(enemy_id)
        if enemy is None:
            return jsonify({'error': f"There's no enemy with an id {enemy_id}"}), 404
    else:
        return jsonify({'error': 'cannot find parameter enemy_type'}), 400
    enemy = validate_entity(enemy, enemy_type)
    if isinstance(enemy, Response):
        return enemy
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


def validate_entity(entity, entity_type='character'):
    if entity_type == 'character':
        try:
            return map_dictionary_to_character(entity)
        except OverflowError:
            error_message = (f'For level {entity.get("level")} max number of stat points is '
                             f'{Character.calculate_stat_points_by_level(entity.get("level"))}')
            return make_response(jsonify({'error': error_message}), 400)

    else:
        try:
            return map_dictionary_to_mob(entity)
        except OverflowError:
            error_message = (f'For level {entity.get("level")} max number of stat points is '
                             f'{Character.calculate_stat_points_by_level(entity.get("level"))}')
            return make_response(jsonify({'error': error_message}), 400)


@blueprint.route('/api/v1/character/<character_id>', methods=['PATCH'])
def update_character(character_id):
    character = character_repository.find_by_id(character_id)
    if character is None:
        return jsonify({'error': f"There's no character with an id {character_id}"}), 404
    else:
        data = request.get_json()
        for key, value in data.items():
            character[key] = value
        character_repository.update_character(map_dictionary_to_character(character))
        return jsonify({'character': character})


@blueprint.route('/api/v1/character', methods=['POST'])
def create_character():
    data = request.get_json()
    character = validate_entity(data)
    if isinstance(character, Response):
        return character
    character_id = character_repository.add_character(character)
    return jsonify({'character_id': character_id})


@blueprint.route('/api/v1/character/max_stat_points/<level>')
def get_max_stat_points(level):
    try:
        max_stat_points = Character.calculate_stat_points_by_level(int(level))
    except ValueError:
        return jsonify({'error': f'{level} must be a number'}), 400
    return jsonify({'max_stat_points': max_stat_points})


@blueprint.route('/api/v1/character/random/<level>/<playability>')
def get_random_character(level, playability):
    try:
        level = int(level)
    except ValueError:
        return jsonify({'error': f'{level} must be a number'}), 400
    generated_hero = Character(playability=playability, xp=0, level=level)
    generated_hero = map_character_to_dictionary(generated_hero)
    return jsonify({'generated_hero': generated_hero})
