import math


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
