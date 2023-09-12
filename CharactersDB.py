import random

import psycopg2


class Character:
    def __init__(self, name):
        self.name = name
        self.critical_attack = random.randint(1, 10)
        self.health = random.randint(50, 100)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(5, 20)
        self.luck = random.randint(1, 10)

        # Создать персонажа в базе данных
        self.create_in_database()

    def create_in_database(self):
        connection = psycopg2.connect(
            host="localhost",
            database="CharactersDB",
            user="postgres",
            password="Ваш пароль"
        )
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO characters (name, critical_attack, health, armor, attack, luck)"
            " VALUES (%s, %s, %s, %s, %s, %s)",
            (self.name, self.critical_attack, self.health, self.armor, self.attack, self.luck)
        )
        connection.commit()

        cursor.close()
        connection.close()

    def update_stats(self):
        # Обновить характеристики персонажа в базе данных
        connection = psycopg2.connect(
            host="localhost",
            database="CharactersDB",
            user="postgres",
            password="Ваш пароль"
        )
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE characters SET critical_attack = %s, health = %s, armor = %s,"
            " attack = %s, luck = %s WHERE name = %s",
            (self.critical_attack, self.health, self.armor, self.attack, self.luck, self.name)
        )
        connection.commit()

        cursor.close()
        connection.close()

    def __str__(self):
        return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}," \
               f" броня {self.armor}, атака {self.attack}, удача {self.luck}"


def generate_characters(num_characters):
    character_list = []
    character_names = ["Character1", "Character2"]  # Замените на реальные имена персонажей
    for i in range(num_characters):
        name = random.choice(character_names)
        character_list.append(Character(name))
    return character_list


characters = generate_characters(2)
for character in characters:
    print(character)
