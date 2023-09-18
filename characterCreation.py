import random

from faker import Faker


class Character:
    def __init__(self):
        fake = Faker()
        self.name = fake.name()
        self.level = 1
        self.xp = 0
        self.health = random.randint(70, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(5, 20)
        self.luck = random.randint(1, 10)
        self.balance = 0
        self.alive = True
        self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack

    def take_damage(self, damage):
        actual_damage = max(damage - self.armor, 0)
        self.health -= actual_damage

    def reset_luck(self):
        self.luck = random.randint(1, 10)
        self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack

    def reset_attack(self):
        self.attack = random.randint(1, 20 * self.level)

    def __str__(self):
        return (f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, "
                f"атака {self.attack}, удача {self.luck}")


character1 = Character()
character2 = Character()
