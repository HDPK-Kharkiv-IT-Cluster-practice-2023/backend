import psycopg2
from psycopg2 import extras


class MobRepository:
    def __init__(self):
        self.connection_creds = {
            'host': 'localhost',
            'database': 'charactersdb',
            'user': 'postgres',
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
            "INSERT INTO mob_types (mob_name, level, xp, max_health, health, armor, attack, luck, balance, alive, "
            "critical_attack)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
             character.attack, character.luck, character.balance, character.alive, character.critical_attack)
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
            "UPDATE mob_types SET mob_name = %s, level = %s, xp = %s, max_health = %s, health = %s , armor = %s, "
            "attack = %s, luck = %s, balance = %s, alive = %s, critical_attack = %s WHERE id = %s",
            (character.name, character.level, character.xp, character.max_health, character.health, character.armor,
             character.attack, character.luck, character.balance, character.alive, character.critical_attack,
             character.id)
        )
        connection.commit()

        cursor.close()
        connection.close()

    def add_all(self, characters_list):
        connection = self._create_connection()
        cursor = connection.cursor()
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
        cursor.close()
        connection.close()

    def exist_by_id(self, character_id):
        connection = self._create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM mob_types WHERE id = %s", (character_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count > 0

    def find_all(self):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM mob_types")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

    def find_all_by_alive(self, alive=True):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM mob_types "
                       "WHERE alive = %s ", (alive,))
        records = cursor.fetchall()
        records_dict = [dict(record) for record in records]
        cursor.close()
        connection.close()
        return records_dict

    def find_all_by_alive_and_level(self, level, alive=True):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM mob_types "
                       "WHERE level = %s "
                       "AND alive = %s", (level, alive))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

    def find_by_id(self, character_id):
        connection = self._create_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM mob_types WHERE id = %s", (character_id,))
        record = cursor.fetchone()
        records_dict = dict(record)
        cursor.close()
        connection.close()
        return records_dict

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
