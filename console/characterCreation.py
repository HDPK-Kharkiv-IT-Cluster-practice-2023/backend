import random
from faker import Faker
from models.Dice import Dice
from models.HealthBar import HealthBar
from models.XpBar import XpBar


class Character:
    def __init__(self, id=None, name=None, level=1, xp=None, max_health=None, health=None,
                 armor=None, attack=None, luck=None, balance=0,
                 alive=True, critical_attack=2, playability=False):
        fake = Faker()
        self.dice = Dice()
        self.id = id
        self.name = name if name else fake.name()
        self.level = level
        self.xp_goal = self.calculate_xp_by_level()
        self._xp = xp if xp is not None else random.randint(self.xp_goal // 4, self.xp_goal // 2)
        self.max_health = max_health if max_health else random.randint(70, 100 + (level - 1) * 10)
        self._health = health if health else self.max_health
        self.armor = armor if armor else random.randint(1, 10 + (level - 1) * 5)
        self.attack = attack if attack else random.randint(5, 20 + (level - 1) * 5)
        self.luck = luck if luck else random.randint(1, 10 + (level - 1) * 2)
        self.balance = balance
        self.alive = alive
        self.critical_attack = critical_attack
        self.playability = playability
        self.health_bar = HealthBar(self)
        self.xp_bar = XpBar(self)

    def calculate_xp_by_level(self):
        base_xp_goal = 100
        return base_xp_goal + (self.level - 1) * 25

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

    def gain_xp(self, xp_amount):
        self.xp += xp_amount
        if self.xp >= self.xp_goal:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += random.randint(5, 10)
        if self.health < self.max_health:
            self.health = self.max_health
        self.armor += random.randint(0, 5)
        self.attack += random.randint(0, 5)
        self.luck += random.randint(0, 2)
        self.xp -= self.xp_goal
        self.xp_goal = self.calculate_xp_by_level()
        if not self.playability and self.xp == 0:
            self.xp = random.randint(self.xp_goal // 4, self.xp_goal // 2)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.health_bar.update_health(self)

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, value):
        self._xp = value
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
        return (f'{self.name}\n'
                f'{self.health_bar}\n'
                f'Level: {self.xp_bar}\n'
                f'Attack: {self.attack}, '
                f'Armor: {self.armor}, '
                f'Luck: {self.luck}, '
                f'Crit: {self.critical_attack}, '
                f'Balance: {self.balance}\n')

# character1 = CharacterRepository()
# character2 = CharacterRepository()
