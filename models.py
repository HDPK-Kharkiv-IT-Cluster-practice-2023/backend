import random
import math


class Dice:
    def __init__(self, min=0, max=100):
        self.min = min
        self.max = max

    def roll_dice(self):
        return random.randint(self.min, self.max)


class HealthBar:
    def __init__(self, character, bar_length=30):
        self.max_health = 0
        self.current_health = 0
        self.damage = 0
        self.extra_life = 0
        self.bar_length = bar_length
        self.update_health(character)

    def update_health(self, character):
        if character.health < 0:
            raise ValueError("current_health can't be negative")
        extra_life = 0
        damage = 0
        if character.health > character.max_health:
            extra_life = character.health - character.max_health
        elif self.current_health > character.health:
            damage = self.current_health - character.health - self.extra_life
        elif self.current_health == character.health:
            damaged_length = self.bar_length * self.damage / self.max_health
            filled_length = self.bar_length * self.current_health / self.max_health
            if not damaged_length == math.ceil(damaged_length) and math.ceil(filled_length) == self.bar_length:
                damage = 1
        self.max_health = character.max_health
        self.current_health = character.health
        self.damage = damage
        self.extra_life = extra_life

    @staticmethod
    def _colored_text(text, color_code):
        return f"\033[{color_code}" + "{}".format(text) + "\033[0m{}".format('')

    def __str__(self):
        progress = (self.current_health - self.extra_life) / self.max_health
        damage_progress = self.damage / self.max_health
        extra_progress = self.extra_life / self.max_health

        filled_length = math.floor(self.bar_length * progress)
        damaged_length = math.ceil(self.bar_length * damage_progress)
        extra_filled_length = math.ceil(self.bar_length * extra_progress)

        filled_text = '█' * filled_length
        damaged_text = '█' * damaged_length
        end_text = '-' * (self.bar_length - filled_length - damaged_length)
        extra_filled_text = '█' * extra_filled_length

        colored_damaged_text = HealthBar._colored_text(damaged_text, '31m')
        colored_extra_filled_text = HealthBar._colored_text(extra_filled_text, '32m')

        bar = f"{filled_text}{colored_damaged_text}{end_text}{colored_extra_filled_text}"
        return f'[{bar}] {self.current_health}/{self.max_health} HP'

class XpBar:
    def __init__(self, character, bar_length=10):
        self.level = character.level
        self.curr_xp = character.xp
        self.xp_goal = character.xp_goal
        self.bar_length = bar_length

    def update_xp(self, character):
        self.level = character.level
        self.curr_xp = character.xp
        self.xp_goal = character.xp_goal

    def __str__(self):
        progress = self.curr_xp / self.xp_goal
        filled_length = math.ceil(self.bar_length * progress)
        if filled_length == 0:
            return f'{self.level}'
        filled_text = '━' * filled_length
        end_text = ' ' * (self.bar_length - filled_length)
        bar = f"{filled_text}{end_text}"
        return f'{self.level} {bar} {self.level + 1}'
