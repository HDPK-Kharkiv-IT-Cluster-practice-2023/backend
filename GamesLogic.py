import random
from faker import Faker

class Player:
    def __init__(self):
        self.health = 50
        self.armor = random.randint(1, 10)

class Character:
    def __init__(self, name):
        self.name = name  # Don't generate a random name here, use the provided name.
        self.critical_attack = random.randint(1, 10)
        self.health = random.randint(70, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(10, 20)
        self.luck = random.randint(1, 10)
        self.alive = True

    def __str__(self):
        return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, атака {self.attack}, удача {self.luck}"

class Fight(object):
    def __init__(self, character1, character2, player):
        self.character1 = character1
        self.character2 = character2
        self.player = player  # Store the player object as an instance variable

    def enter(self):
        character1.alive = True
        character2.alive = True

        def armor_calculated(character, player):
            calculated = character.attack - player.armor
            if calculated <= 0:
                return 0
            else:
                return calculated

        print("\n" + "-" * 10)
        print(f"Тут два вороги: {self.character1.name} і {self.character2.name}")
        print(f"{self.character1.name} має {self.character1.health} очок здоров'я, атака {self.character1.attack}")
        print(f"{self.character2.name} має {self.character2.health} очок здоров'я, атака {self.character2.attack}")
        print(f"Ви маєте {self.player.health} здоров'я та {self.player.armor} бронi")

        while self.player.health > 0 and (character1.alive or character2.alive):
            print("\n" + "-" * 10)
            your_attack = random.randint(4, 12)

            def oooo(character1, character2, mainAttack=your_attack):
                attack = input(f"Натисніть 1, щоб атакувати {self.character1.name}, 2, щоб атакувати {self.character2.name} >")
                if attack == "1":
                    if character1.alive:
                        character1.health -= mainAttack
                        print(f"Ви нанесли {character1.name} {mainAttack} очок урону.")
                        if character1.health <= 0:
                            character1.alive = False
                            print(f"{character1.name} вбитий!")
                    else:
                        print(f"{character1.name} вже мертвий!")
                elif attack == "2":
                    if character2.alive:
                        character2.health -= mainAttack
                        print(f"Ви нанесли {character2.name} {mainAttack} очок урону.")
                        if character2.health <= 0:
                            character2.alive = False
                            print(f"{self.character2.name} вбитий!")
                    else:
                        print(f"{character2.name} вже мертвий!")
                else:
                    print("Проґавив.")

            oooo(self.character1, self.character2)

            def characterFight(character):
                if character.alive:
                    with_armor = armor_calculated(character, self.player)  # Pass self.player as an argument
                    self.player.health -= with_armor  # Update the player's health
                    print(f"{character.name} б'є вас на {character.attack} ({with_armor} пiсля бронi) очок, у вас залишилося {self.player.health} очок життя, у {character.name} залишилося {character.health} здоров'я.")
                if character.health <= 0:
                    character.alive = False
                    print(f"{character.name} вбитий!")
                if self.player.health <= 0:
                    print("Ви померли.")

            characterFight(self.character1)
            characterFight(self.character2)

# Створення персонажiв
character1 = Character("Персонаж 1")
character2 = Character("Персонаж 2")
player = Player()

# Створення гри та передача персонажiв
a_fight = Fight(character1, character2, player)
a_fight.enter()
