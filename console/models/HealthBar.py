import math


class HealthBar:
    def __init__(self, max_health, curr_health, bar_length=30):
        if max_health <= 0:
            raise ValueError("max_health must be a positive number")
        self.max_health = max_health
        self.curr_health = curr_health
        self.damage = 0
        self.bar_length = bar_length

    def update_health(self, curr_health):
        if curr_health < 0:
            raise ValueError("curr_health can't be negative")
        difference = curr_health - self.curr_health
        if difference == 0:
            self.damage = 0
        elif difference > 0:
            self.curr_health += difference
            self.damage = 0
        else:
            self.curr_health += difference
            if self.curr_health + abs(difference) > self.max_health:
                extra_damage = self.curr_health + abs(difference) - self.max_health
                self.damage = abs(difference) - extra_damage
            else:
                self.damage = abs(difference)

    @staticmethod
    def _colored_text(text, color_code):
        return f"\033[{color_code}" + "{}".format(text) + "\033[0m{}".format('')

    def __str__(self):
        if self.curr_health > self.max_health:
            extra_life = self.curr_health - self.max_health
            curr_health = self.curr_health - extra_life
            self.damage = 0
        else:
            extra_life = 0
            curr_health = self.curr_health

        progress = curr_health / self.max_health
        damage_progress = self.damage / self.max_health
        extra_progress = extra_life / self.max_health

        filled_length = math.ceil(self.bar_length * progress)
        damaged_length = math.floor(self.bar_length * damage_progress)
        extra_filled_length = math.ceil(self.bar_length * extra_progress)

        filled_text = '█' * filled_length
        damaged_text = '█' * damaged_length
        end_text = '-' * (self.bar_length - filled_length - damaged_length)
        extra_filled_text = '█' * extra_filled_length

        colored_filled_text = HealthBar._colored_text(filled_text, '0m')
        colored_damaged_text = HealthBar._colored_text(damaged_text, '31m')
        colored_extra_filled_text = HealthBar._colored_text(extra_filled_text, '32m')

        bar = f"{colored_filled_text}{colored_damaged_text}{end_text}{colored_extra_filled_text}"
        return f'[{bar}] {self.curr_health}/{self.max_health} HP'
