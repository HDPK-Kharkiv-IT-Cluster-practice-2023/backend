import random
from faker import Faker


class Player:
    def __init__(self):
        self.health = 100
        self.your_armor = random.randint(1, 10)
        self.your_attack = random.randint(10, 20)

    def take_damage(self, damage):
        actual_damage = max(damage - self.your_armor, 0)
        self.health -= actual_damage

    def reset_your_attack(self):
        self.your_attack = random.randint(1, 20)


Player_you = Player()


class Character:
    def __init__(self):
        fake = Faker()
        self.name = fake.name()
        self.critical_attack = random.randint(1, 10)
        self.health = random.randint(70, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(5, 20)
        self.luck = random.randint(1, 10)
        self.alive = True

    def take_damage(self, damage):
        actual_damage = max(damage - self.armor, 0)
        self.health -= actual_damage

    def reset_attack(self):
        self.attack = random.randint(1, 20)

    def __str__(self):
        return (f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, "
                f"атака {self.attack}, удача {self.luck}")


character1 = Character()
character2 = Character()