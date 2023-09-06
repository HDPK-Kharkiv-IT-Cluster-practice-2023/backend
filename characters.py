import random
#characters.py

class Character:
    def __init__(self, name):
        self.name = name
        self.critical_attack = random.randint(5, 10)
        self.health = 100
        self.armor = random.randint(5, 10)
        self.attack = random.randint(10, 20)
        self.luck = random.randint(5, 10)

    def __str__(self):
        return f"{self.name}: критична атака {self.critical_attack}, здоров'я {self.health}, броня {self.armor}, атака {self.attack}, вдача {self.luck}"

    def take_damage(self, damage):
        # Calculate damage
        actual_damage = damage - self.armor
        self.health -= actual_damage