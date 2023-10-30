import psycopg2
from psycopg2 import extras
from repository.db_manager import DatabaseManager
from psycopg2.errors import InvalidTextRepresentation


class MobRepository:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def _create_in_database(self, character):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO mob_types (mob_name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
                "critical_attack)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                 character.attack, character.luck, character.balance, character.alive, character.critical_attack)
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
                "UPDATE mob_types SET mob_name = %s, level = %s, xp = %s, max_health = %s, health = %s , armor = %s, "
                "attack = %s, luck = %s, balance = %s, alive = %s, critical_attack = %s WHERE id = %s",
                (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                 character.attack, character.luck, character.balance, character.alive, character.critical_attack,
                 character.id)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def add_all(self, characters_list):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            for character in characters_list:
                cursor.execute(
                    "INSERT INTO mob_types (mob_name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
                    "critical_attack)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
                     character.attack, character.luck, character.balance, character.alive, character.critical_attack)
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
            cursor.execute("SELECT COUNT(*) FROM mob_types WHERE id = %s", (character_id,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
            connection.close()

    def find_all(self):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM mob_types")
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()

    def find_all_by_alive(self, alive=True):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM mob_types "
                           "WHERE alive = %s ", (alive,))
            records = cursor.fetchall()
            records_dict = [dict(record) for record in records]
            return records_dict
        finally:
            cursor.close()
            connection.close()

    def find_all_by_alive_and_level(self, level, alive=True):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM mob_types "
                           "WHERE level = %s "
                           "AND alive = %s", (level, alive))
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, character_id):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM mob_types WHERE id = %s", (character_id,))
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

    def add_mob(self, character):
        if character.id is None:
            new_id = self._create_in_database(character)
            character.id = new_id
            return new_id
        else:
            return False

    def update_mob(self, character):
        if self.exist_by_id(character.id):
            self._update_stats(character)
            return True
        else:
            return False

#     def __str__(self):
#         return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}
#         , " \f"атака {self.attack}, удача {self.luck}"
#
#
# def generate_mobs(num_mobs):
#     mob_list = []
#     mob_names = ["Zombie", "Skeleton", "Spider", "Slime", "Goblin"]
#     for i in range(num_mobs):
#         name = random.choice(mob_names)
#         mob_list.append(Mob(name))
#     return mob_list
#
#
# mobs = generate_mobs(10)
# for mob in mobs:
#     print(mob)