import random
from faker import Faker


class Player:
    def __init__(self):
        self.health = 100
        self.armor = random.randint(1, 10)
        self.yourattack = random.randint(10, 20)


class Character:
    def __init__(self, name):
        # Don't generate a random name here, use the provided name.
        fake = Faker()
        self.name = fake.name()
        self.critical_attack = random.randint(1, 10)
        self.health = random.randint(70, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(10, 20)
        self.luck = random.randint(1, 10)
        self.alive = True


class Fight(object):
    def __init__(self, character1, character2, player):
        self.character1 = character1
        self.character2 = character2
        self.player = player  # Store the player object as an instance variable

    def enter(self):
        character1.alive = True
        character2.alive = True

        def characterArmor_calculated(character, player):
            calculated = player.yourattack - character.armor
            if calculated <= 0:
                return 0
            else:
                return calculated

        def armor_calculated(character, player):
            calculated = character.attack - player.armor
            if calculated <= 0:
                return 0
            else:
                return calculated

        print("\n" + "-" * 10)
        print(
            f"Тут два вороги: {self.character1.name} і {self.character2.name}")
        print(f"{self.character1.name} має {self.character1.health} очок здоров'я, {self.character1.armor} бронi, атака {self.character1.attack}")
        print(f"{self.character2.name} має {self.character2.health} очок здоров'я, {self.character2.armor} бронi, атака {self.character2.attack}")
        print(
            f"Ви маєте {self.player.health} здоров'я та {self.player.armor} бронi, ваша атака {self.player.yourattack}")

        while self.player.health > 0 and (character1.alive or character2.alive):
            print("\n" + "-" * 10)

            def playerFightsCharacters(character1, character2, player):
                attack = input(
                    f"Натисніть 1, щоб атакувати {self.character1.name}, 2, щоб атакувати {self.character2.name} >")
                if attack == "1":
                    if character1.alive:
                        withCharacter_armor = characterArmor_calculated(
                            character1, self.player)
                        character1.health -= withCharacter_armor
                        print(
                            f"Ви нанесли {character1.name} {player.yourattack} (з вразуванням бронi: {withCharacter_armor}) очок урону.")
                        if character1.health <= 0:
                            character1.alive = False
                            print(f"{character1.name} вбитий!")
                    else:
                        print(f"{character1.name} вже мертвий!")
                elif attack == "2":
                    if character2.alive:
                        withCharacter_armor1 = characterArmor_calculated(
                            character2, self.player)
                        character2.health -= withCharacter_armor1
                        print(
                            f"Ви нанесли {character2.name} {player.yourattack}(з вразуванням бронi: {withCharacter_armor1}) очок урону.")
                        if character2.health <= 0:
                            character2.alive = False
                            print(f"{self.character2.name} вбитий!")
                    else:
                        print(f"{character2.name} вже мертвий!")
                else:
                    print("Проґавив.")

            playerFightsCharacters(
                self.character1, self.character2, self.player)

            def characterFightsPlayer(character):
                if character.alive:
                    # Pass self.player as an argument
                    with_armor = armor_calculated(character, self.player)
                    self.player.health -= with_armor  # Update the player's health
                    print(f"{character.name} б'є вас на {character.attack} ({with_armor} пiсля бронi) очок, у вас залишилося {self.player.health} очок життя, у {character.name} залишилося {character.health} здоров'я.")
                if character.health <= 0:
                    character.alive = False
                    print(f"{character.name} вбитий!")
                if self.player.health <= 0:
                    print("Ви померли.")

            characterFightsPlayer(self.character1)
            characterFightsPlayer(self.character2)


# Створення персонажiв
character1 = Character("Персонаж 1")
character2 = Character("Персонаж 2")
player = Player()

# Створення гри та передача персонажiв
a_fight = Fight(character1, character2, player)
a_fight.enter()
