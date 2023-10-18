def map_mob_to_dictionary(mob):
    return {
        'id': mob.id,
        'mob_name': mob.name,
        'level': mob.level,
        'xp': mob.xp,
        'max_health': mob.max_health,
        'health': mob.health,
        'armor': mob.armor,
        'attack': mob.attack,
        'luck': mob.luck,
        'balance': mob.balance,
        'alive': mob.alive,
        'critical_attack': mob.critical_attack
    }


def map_character_to_dictionary(character):
    return {
        'id': character.id,
        'name': character.name,
        'level': character.level,
        'xp_goal': character.xp_goal,
        'xp': character.xp,
        'max_health': character.max_health,
        'health': character.health,
        'armor': character.armor,
        'attack': character.attack,
        'luck': character.luck,
        'balance': character.balance,
        'alive': character.alive,
        'critical_attack': character.critical_attack,
        'playability': character.playability
    }

