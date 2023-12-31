import random
from models import Dice
from models import HealthBar


class Mob:
    def __init__(self, character=None, id=None, name=None, level=None, xp=None, max_health=None, health=None,
                 armor=None, attack=None, luck=None, balance=0,
                 alive=True, critical_attack=2):
        mob_names = ["Zombie", "Skeleton", "Spider", "Slime", "Goblin"]
        self.name = name if name else random.choice(mob_names)
        self.dice = Dice()
        self.id = id
        self.level = level if level is not None else character.level
        self.xp = xp if xp is not None else random.randint(character.xp_goal // 4, character.xp_goal // 2)
        self.max_health = max_health
        self._health = health if health is not None else self.max_health
        self.armor = armor
        self.attack = attack
        self.luck = luck
        self.balance = balance
        self.alive = alive
        self.critical_attack = critical_attack
        self.health_bar = None

        self.init_stats()

    def init_stats(self):
        if any(getattr(self, attr) is None for attr in ['max_health', 'armor', 'attack', 'luck']):
            points = self.point_spread()
            self.luck = points
        self.health = self.max_health
        self.health_bar = HealthBar(self)

    def point_spread(self):
        points = self.calculate_stat_points_by_level(self.level)
        self.max_health = random.randint(15, 20 + (self.level - 1) * 2)
        self.health = self.max_health
        self.attack = random.randint(1, 10 + (self.level - 1) * 2)
        self.armor = random.randint(0, 5 + (self.level - 1) * 1)
        points -= self.max_health + self.armor + self.attack
        if points < 0:
            points = self.point_spread()
        return points

    def take_damage(self, character):
        if not character.alive:
            return
        if self.dice.roll_dice() > character.luck:
            damage = character.attack
        else:
            damage = character.attack * character.critical_attack
        actual_damage = max(damage - self.armor, 0)
        if actual_damage >= self.health:
            self.health = 0
            self.alive = False
            character.gain_xp(self.xp)
            character.update_bars()
            self.xp = 0
        else:
            self.health -= actual_damage

    @staticmethod
    def calculate_stat_points_by_level(level):
        base_stat_points = 40
        return base_stat_points + (level - 1) * 5

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        if self.health_bar is not None:
            self.health_bar.update_health(self)

    def update_bars(self):
        self.health_bar.update_health(self)

    # def reset_luck(self):
    #     self.luck = random.randint(1, 10)
    #     self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack
    #
    # def reset_attack(self):
    #     self.attack = random.randint(1, 20 * self.level)

    def __str__(self):
        if self.health_bar is None:
            self.health_bar = f'Health: {self.health}/{self.max_health}'
        return (f'{self.name}\n'
                f'{self.health_bar}\n'
                f'Level: {self.level}\n'
                f'Attack: {self.attack}, '
                f'Armor: {self.armor}, '
                f'Luck: {self.luck}, '
                f'Crit: {self.critical_attack}, '
                f'Balance: {self.balance}\n')

