import random
from faker import Faker

class Character:
    def __init__(self, name):
        fake = Faker()
        self.name = fake.name()
        self.critical_attack = random.randint(1, 10)
        self.health = random.randint(70, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(5, 20)
        self.luck = random.randint(1, 10)

    def __str__(self):
        return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, атака {self.attack}, удача {self.luck}"

class Fight(object):
    def __init__(self, character1, character2):
        self.character1 = character1
        self.character2 = character2

    def enter(self):
        print("\n" + "-" * 10)
        print(f"Тут два вороги: {self.character1.name} і {self.character2.name}")
        print(f"{self.character1.name} має {self.character1.health} очок здоров'я, атака {self.character1.attack}")
        print(f"{self.character2.name} має {self.character2.health} очок здоров'я, атака {self.character2.attack}")

        your_hit_points = 50
        character1_hit_points = self.character1.health
        character2_hit_points = self.character2.health
        character1_alive = True
        character2_alive = True

        while your_hit_points > 0 and (character1_alive or character2_alive):
            print("\n" + "-" * 10)
            your_attack = random.randint(4, 12)
            character1_attack = random.randint(1, 4)
            character2_attack = random.randint(4, 8)

            attack = input(f"Натисніть 1, щоб атакувати {self.character1.name}, 2, щоб атакувати {self.character2.name} >")
            if attack == "1":
                if character1_alive:
                    character1_hit_points -= your_attack
                    print(f"Ви нанесли {self.character1.name} {your_attack} очок урону.")
                    if character1_hit_points <= 0:
                        character1_alive = False
                        print(f"{self.character1.name} вбитий!")
                else:
                    print(f"{self.character1.name} вже мертвий!")
            elif attack == "2":
                if character2_alive:
                    character2_hit_points -= your_attack
                    print(f"Ви нанесли {self.character2.name} {your_attack} очок урону.")
                    if character2_hit_points <= 0:
                        character2_alive = False
                        print(f"{self.character2.name} вбитий!")
                else:
                    print(f"{self.character2.name} вже мертвий!")
            else: 
                print("Проґавив.")

            if character1_alive:
                your_hit_points -= character1_attack
                print(f"{self.character1.name} б'є вас на {character1_attack} очок, у вас залишилося {your_hit_points} очок життя, у {self.character1.name} залишилося {character1_hit_points} здоров'я.")
                if character1_hit_points <= 0:
                    character1_alive = False
                    print(f"{self.character1.name} вбитий!")
            if character2_alive:
                your_hit_points -= character1_attack
                print(f"{self.character2.name} б'є вас на {character2_attack} очок, у вас залишилося {your_hit_points} очок життя, у {self.character2.name} залишилося {character2_hit_points} здоров'я.")
                if character2_hit_points <= 0:
                    character2_alive = False
                    print(f"{self.character2.name} вбитий!")

            if your_hit_points <= 0:
                print("Ви померли.")
                break

# Створення персонажiв
character1 = Character("Персонаж 1")
character2 = Character("Персонаж 2")

# Створення гри та передача персонажiв
a_fight = Fight(character1, character2)
a_fight.enter()
