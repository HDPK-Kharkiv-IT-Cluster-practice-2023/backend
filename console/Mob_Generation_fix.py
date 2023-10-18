import random
from faker import Faker
from models.Dice import Dice
from models.HealthBar import HealthBar
from models.XpBar import XpBar


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
        self.max_health = max_health if max_health else random.randint(70, 100 + (self.level - 1) * 10)
        self._health = self.max_health
        self.armor = armor if armor else random.randint(1, 10 + (self.level - 1) * 3)
        self.attack = attack if attack else random.randint(5, 20 + (self.level - 1) * 3)
        self.luck = luck if luck else random.randint(1, 10 + (self.level - 1) * 1)
        self.balance = balance
        self.alive = alive
        self.critical_attack = critical_attack
        self.health_bar = HealthBar(self)

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

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
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


# mob1 = Mob()
# print(mob1)
