import random
from faker import Faker
from models import Dice
from models import HealthBar
from models import XpBar
import json


class Character:
    def __init__(self, id=None, name=None, level=1, xp=None, max_health=None, health=None,
                 armor=None, attack=None, luck=None, balance=0,
                 alive=True, critical_attack=2, playability=False, stat_points=None):
        fake = Faker()
        self.dice = Dice()
        self.id = id
        self.name = name if name else fake.name()
        self.level = level
        self.stat_points = stat_points if stat_points is not None else self.calculate_stat_points_by_level(self.level)
        self.xp_goal = self.calculate_xp_by_level()
        self._xp = xp if xp is not None else random.randint(self.xp_goal // 4, self.xp_goal // 2)
        self.max_health = max_health
        self._health = health if health else self.max_health
        self.attack = attack
        self.armor = armor
        self.luck = luck
        self.balance = balance if balance is not None else 0
        self.alive = alive
        self.critical_attack = critical_attack if critical_attack is not None else 2
        self.playability = playability
        self.health_bar = None
        self.xp_bar = None

        self.init_stats()

    def calculate_points_balance(self):
        points = self.calculate_stat_points_by_level(self.level)
        points -= self.max_health + self.armor + self.attack + self.luck
        if points < 0:
            raise OverflowError
        else:
            self.stat_points = points

    def init_stats(self):
        if any(getattr(self, attr) is None for attr in ['max_health', 'armor', 'attack', 'luck']):
            points = self.point_spread()
            self.luck = points
        self.health_bar = HealthBar(self)
        self.xp_bar = XpBar(self)
        self.calculate_points_balance()

    def point_spread(self):
        points = self.calculate_stat_points_by_level(self.level)
        self.max_health = random.randint(15, 35 + (self.level - 1) * 2)
        self.health = self.max_health
        self.attack = random.randint(1, 10 + (self.level - 1) * 2)
        self.armor = random.randint(0, 10 + (self.level - 1) * 1)
        points -= self.max_health + self.armor + self.attack
        if points < 0:
            points = self.point_spread()
        return points

    def generate_random_stat_by_level(self, min, max, increase_by_level=0):
        stat_value = random.randint(min, max + (self.level - 1) * increase_by_level)
        if self.stat_points < stat_value:
            stat_value = self.stat_points
        self.stat_points -= stat_value
        return stat_value

    def calculate_xp_by_level(self):
        base_xp_goal = 100
        return base_xp_goal + (self.level - 1) * 25

    @staticmethod
    def calculate_stat_points_by_level(level):
        base_stat_points = 50
        return base_stat_points + (level - 1) * 5

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
            if isinstance(character, Character):
                character.gain_xp(self.xp)
                character.update_bars()
            self.xp = 0
        else:
            self.health -= actual_damage

    def gain_xp(self, xp_amount):
        self.xp += xp_amount
        if self.xp >= self.xp_goal:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_goal
        self.xp_goal = self.calculate_xp_by_level()
        if not self.playability:
            self.skills_up(self.max_health + 2, self.armor + 1, self.attack + 1, self.luck + 1)
            if self.xp == 0:
                self.xp = random.randint(self.xp_goal // 4, self.xp_goal // 2)
        else:
            self.calculate_points_balance()

    def skills_up(self, new_max_health, new_armor, new_attack, new_luck):
        if new_max_health + new_armor + new_attack + new_luck > self.calculate_stat_points_by_level(self.level):
            raise OverflowError
        self.max_health = new_max_health
        if self.health < self.max_health:
            self.health = self.max_health
        self.armor = new_armor
        self.attack = new_attack
        self.luck = new_luck
        self.calculate_points_balance()
        self.update_bars()

    def toJSON(self):
        character_dict = {
            "id": self.id,
            "name": self.name,
            "criticalAttack": self.critical_attack,
            "health": self.health,
            "armor": self.armor,
            "attack": self.attack,
            "luck": self.luck,
            "level": self.level,
            "xp": self.xp,
            "balance": self.balance,
            "alive": self.alive,
            "playability": self.playability,
            "maxHealth": self.max_health
        }
        return json.dumps(character_dict, sort_keys=False, indent=4)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        if self.health_bar is not None:
            self.health_bar.update_health(self)

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, value):
        self._xp = value
        if self.xp_bar is not None:
            self.xp_bar.update_xp(self)

    def update_bars(self):
        self.xp_bar.update_xp(self)
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
        if self.xp_bar is None:
            self.xp_bar = f'{self.level} - {self.xp / self.xp_goal * 100}%'
        points = ''
        if self.playability:
            points = f', Points: {self.stat_points}'
        return (f'{self.name}\n'
                f'{self.health_bar}\n'
                f'Level: {self.xp_bar}\n'
                f'Attack: {self.attack}, '
                f'Armor: {self.armor}, '
                f'Luck: {self.luck}, '
                f'Crit: {self.critical_attack}, '
                f'Balance: {self.balance}'
                f'{points}\n')
