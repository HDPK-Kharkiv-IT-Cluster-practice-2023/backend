import random

class Character:
    def __init__(self, name):
        self.name = name
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
        print(f"Тут два мачо: {self.character1.name} і {self.character2.name}")
        print(f"{self.character1.name} має {self.character1.health} очок здоров'я, атака {self.character1.attack}")
        print(f"{self.character2.name} має {self.character2.health} очок здоров'я, атака {self.character2.attack}")
        print("Один з них виглядає пораненим чи щось подібним.")

        your_hit_points = 50
        muchacho1_hit_points = self.character1.health
        muchacho2_hit_points = self.character2.health
        muchacho1_alive = True
        muchacho2_alive = True

        while your_hit_points > 0 and (muchacho1_alive or muchacho2_alive):
            print("\n" + "-" * 10)
            your_attack = random.randint(4, 12)
            muchacho1_attack = random.randint(1, 4)
            muchacho2_attack = random.randint(4, 8)

            attack = input(f"Натисніть 1, щоб атакувати {self.character1.name}, 2, щоб атакувати {self.character2.name} >")
            if attack == "1":
                if muchacho1_alive:
                    muchacho1_hit_points -= your_attack
                    print(f"Ви нанесли {self.character1.name} {your_attack} очок урону.")
                    if muchacho1_hit_points <= 0:
                        muchacho1_alive = False
                        print(f"{self.character1.name} вбитий!")
                else:
                    print(f"{self.character1.name} вже мертвий!")
            elif attack == "2":
                if muchacho2_alive:
                    muchacho2_hit_points -= your_attack
                    print(f"Ви нанесли {self.character2.name} {your_attack} очок урону.")
                    if muchacho2_hit_points <= 0:
                        muchacho2_alive = False
                        print(f"{self.character2.name} вбитий!")
                else:
                    print(f"{self.character2.name} вже мертвий!")
            else: 
                print("Проґавив.")

            if muchacho1_alive:
                your_hit_points -= muchacho1_attack
                print(f"{self.character1.name} б'є вас на {muchacho1_attack} очок, у вас залишилося {your_hit_points} очок життя, у {self.character1.name} залишилося {muchacho1_hit_points} здоров'я.")
                if muchacho1_hit_points <= 0:
                    muchacho1_alive = False
                    print(f"{self.character1.name} вбитий!")
            if muchacho2_alive:
                your_hit_points -= muchacho1_attack
                print(f"{self.character2.name} б'є вас на {muchacho2_attack} очок, у вас залишилося {your_hit_points} очок життя, у {self.character2.name} залишилося {muchacho2_hit_points} здоров'я.")
                if muchacho2_hit_points <= 0:
                    muchacho2_alive = False
                    print(f"{self.character2.name} вбитий!")

            if your_hit_points <= 0:
                print("You are dead.")
                break

# Создание персонажей
character1 = Character("Персонаж 1")
character2 = Character("Персонаж 2")

# Создание игры и передача персонажей
a_fight = Fight(character1, character2)
a_fight.enter()
