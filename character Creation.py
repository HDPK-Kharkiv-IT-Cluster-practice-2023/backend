import random

class Character:
    def __init__(self, name):
        self.name = name
        self.critical_attack = random.randint(1, 10)
        self.health = random.randint(50, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(5, 20)
        self.luck = random.randint(1, 10)

    def __str__(self):
        return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, атака {self.attack}, удача {self.luck}"

# Создание персонажей
character1 = Character("Персонаж 1")
character2 = Character("Персонаж 2")

# Вывод информации о персонажах
print(character1)
print(character2)
