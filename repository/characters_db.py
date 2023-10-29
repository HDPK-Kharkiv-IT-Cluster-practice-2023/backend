import psycopg2
from psycopg2 import extras
from psycopg2.errors import InvalidTextRepresentation
from repository.db_manager import DatabaseManager


class CharacterRepository:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def _create_in_database(self, character):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO characters (name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
                "critical_attack, playability, stat_points)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                 character.attack, character.luck, character.balance, character.alive, character.critical_attack,
                 character.playability, character.stat_points)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            return new_id
        finally:
            cursor.close()
            connection.close()

    def _update_stats(self, character):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE characters SET name = %s, level = %s, xp = %s, max_health = %s, health = %s , armor = %s, "
                "attack = %s, luck = %s, balance = %s, alive = %s, critical_attack = %s, playability = %s, "
                "stat_points = %s WHERE id = %s",
                (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                 character.attack, character.luck, character.balance, character.alive, character.critical_attack,
                 character.playability, character.stat_points, character.id)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def add_character_with_user_id(self, character, user_id):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO characters (name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
                "critical_attack, playability, stat_points, owner_id)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                 character.attack, character.luck, character.balance, character.alive, character.critical_attack,
                 character.playability, character.stat_points, user_id)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            return new_id
        finally:
            cursor.close()
            connection.close()

    def add_all(self, characters_list):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            for character in characters_list:
                cursor.execute(
                    "INSERT INTO characters (name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
                    "critical_attack, playability, stat_points)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (character.name, character.level, character.xp, character.max_health, character.health,
                     character.armor, character.attack, character.luck, character.balance, character.alive,
                     character.critical_attack, character.playability, character.stat_points)
                )
                new_id = cursor.fetchone()[0]
                character.id = new_id
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def exist_by_id(self, character_id):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM characters WHERE id = %s", (character_id,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
            connection.close()

    def find_all(self):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM characters')
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()

    def find_all_by_playability_and_alive(self, playability, alive=True):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM characters "
                           "WHERE playability = %s "
                           "AND alive = %s ", (playability, alive))
            records = cursor.fetchall()
            records_dict = [dict(record) for record in records]
            return records_dict
        finally:
            cursor.close()
            connection.close()

    def find_all_by_playability_and_alive_and_level(self, playability, level, alive=True):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM characters "
                           "WHERE level >= 1 AND (level BETWEEN (%s - 1) AND (%s + 1)) "
                           "AND playability = %s "
                           "AND alive = %s", (level, level, playability, alive))
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()

    def find_all_by_user_id_and_alive(self, user_id, alive=True):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM characters "
                           "WHERE owner_id = %s "
                           "AND alive = %s ", (user_id, alive))
            records = cursor.fetchall()
            records_dict = [dict(record) for record in records]
            return records_dict
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, character_id):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM characters WHERE id = %s", (character_id,))
            record = cursor.fetchone()
            if record is None:
                return None
            records_dict = dict(record)
            return records_dict
        except InvalidTextRepresentation:
            return None
        finally:
            cursor.close()
            connection.close()

    def add_character(self, character):
        if character.id is None:
            new_id = self._create_in_database(character)
            character.id = new_id
            return new_id
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
