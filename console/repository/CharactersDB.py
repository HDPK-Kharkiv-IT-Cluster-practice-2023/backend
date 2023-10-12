import psycopg2
from psycopg2 import extras


class CharacterRepository:
    def __init__(self):
        self.connection_creds = {
            'host': 'localhost',
            'database': 'charactersdb',
            'user': 'makswinters',
            'password': 'admin'
        }

    def _create_connection(self):
        return psycopg2.connect(
            host=self.connection_creds.get('host'),
            database=self.connection_creds.get('database'),
            user=self.connection_creds.get('user'),
            password=self.connection_creds.get('password')
        )

    def _create_in_database(self, character):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO characters (name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
            "critical_attack, playability)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
             character.attack, character.luck, character.balance, character.alive, character.critical_attack,
             character.playability)
        )
        new_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()
        return new_id

    def _update_stats(self, character):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE characters SET name = %s, level = %s, xp = %s, max_health = %s, health = %s , armor = %s, "
            "attack = %s, luck = %s, balance = %s, alive = %s, critical_attack = %s, playability = %s WHERE id = %s",
            (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
             character.attack, character.luck, character.balance, character.alive, character.critical_attack,
             character.playability, character.id)
        )
        connection.commit()
        cursor.close()
        connection.close()

    def add_all(self, characters_list):
        connection = self._create_connection()
        cursor = connection.cursor()
        for character in characters_list:
            cursor.execute(
                "INSERT INTO characters (name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
                "critical_attack, playability)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                 character.attack, character.luck, character.balance, character.alive, character.critical_attack,
                 character.playability)
            )
            new_id = cursor.fetchone()[0]
            character.id = new_id
        connection.commit()
        cursor.close()
        connection.close()

    def exist_by_id(self, character_id):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM characters WHERE id = %s", (character_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count > 0

    def find_all(self):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM characters")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

    def find_all_by_playability_and_alive(self, playability, alive=True):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM characters "
                       "WHERE playability = %s "
                       "AND alive = %s ", (playability, alive))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

    def find_all_by_playability_and_alive_and_level(self, playability, level, alive=True):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM characters "
                       "WHERE level >= 1 AND (level BETWEEN (%s - 1) AND (%s + 1)) "
                       "AND playability = %s "
                       "AND alive = %s", (level, level, playability, alive))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

    def find_by_id(self, character_id):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM characters WHERE id = %s", (character_id,))
        record = cursor.fetchone()
        cursor.close()
        connection.close()
        return record

    def add_character(self, character):
        if character.id is None:
            new_id = self._create_in_database(character)
            character.id = new_id
            return True
        else:
            return False

    def update_character(self, character):
        if self.exist_by_id(character.id):
            self._update_stats(character)
            return True
        else:
            return False

    # def __str__(self):
    #     return (f"{self.character.name}: критическая атака {self.character.critical_attack},"
    #             f" здоровье {self.character.health}, броня {self.character.armor}, атака {self.character.attack},"
    #             f" удача {self.character.luck}")

# def generate_characters(num_characters):
#     character_list = []
#     character_names = ["Character1", "Character2"]  # Замените на реальные имена персонажей
#     for i in range(num_characters):
#         name = random.choice(character_names)
#         character_list.append(CharacterRepository(name))
#     return character_list
#
#
# characters = generate_characters(2)
# for character in characters:
#     print(character)
