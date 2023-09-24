import random
from faker import Faker
from models.Dice import Dice


class Character:
    def __init__(self, id=None, name=None, level=1, xp=0, max_health=None, health=None,
                 armor=None, attack=None, luck=None, balance=0,
                 alive=True, critical_attack=2, playability=False):
        fake = Faker()
        self.dice = Dice()
        self.id = id
        self.name = name if name else fake.name()
        self.level = level
        self.xp = xp
        self.xp_goal = xp
        self.max_health = max_health if max_health else random.randint(70, 100)
        self.health = health if health else self.max_health
        self.armor = armor if armor else random.randint(1, 10)
        self.attack = attack if attack else random.randint(5, 20)
        self.luck = luck if luck else random.randint(1, 10)
        self.balance = balance
        self.alive = alive
        self.critical_attack = critical_attack
        self.playability = playability

    def take_damage(self, character):
        if self.dice.roll_dice() > character.luck:
            damage = character.attack
        else:
            damage = character.attack * character.critical_attack
        actual_damage = max(damage - self.armor, 0)
        if actual_damage >= self.health:
            self.health = 0
            self.alive = False
        else:
            self.health -= actual_damage

    # def reset_luck(self):
    #     self.luck = random.randint(1, 10)
    #     self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack
    #
    # def reset_attack(self):
    #     self.attack = random.randint(1, 20 * self.level)

    def __str__(self):
        return (f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, "
                f"атака {self.attack}, удача {self.luck}")


# character1 = CharacterRepository()
# character2 = CharacterRepository()
