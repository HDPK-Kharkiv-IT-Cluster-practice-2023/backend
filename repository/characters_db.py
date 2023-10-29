import psycopg2
from psycopg2 import extras
from psycopg2.errors import InvalidTextRepresentation
from sshtunnel import SSHTunnelForwarder


class CharacterRepository:
    def __init__(self):
        # self.connection_creds = {
        #     'name': 'global',
        #     'host': 'bandydan-3203.postgres.pythonanywhere-services.com',
        #     'port': 13203,
        #     'db_username': 'super',
        #     'db_password': 'U6Tdw8ReM',
        #     'database_name': 'charactersdb',
        #     'ssh_host': 'ssh.pythonanywhere.com',
        #     'ssh_port': 22,
        #     'ssh_username': 'bandydan',
        #     'ssh_password': 'xb6W7LHNJ6!cRKi',
        #     'ssh_private_key_password': 'masterkey',
        #     'ssh_private_key': '/home/vitaly/.ssh/id_rsa'
        # }

        # local database

        self.connection_creds = {
            'name': 'local',
            'host': 'localhost',
            'database': 'charactersdb',
            'user': 'postgres',
            'password': 'admin'
        }

    def _create_connection(self, tunnel):
        if self.connection_creds.get('name') == 'local':
            return psycopg2.connect(
                host=self.connection_creds.get('host'),
                database=self.connection_creds.get('database'),
                user=self.connection_creds.get('user'),
                password=self.connection_creds.get('password')
            )
        else:
            return psycopg2.connect(
                user=self.connection_creds.get('db_username'),
                password=self.connection_creds.get('db_password'),
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                database=self.connection_creds.get('database_name'),
            )

    def _create_tunnel(self):
        if self.connection_creds.get('name') == 'local':
            return None
        else:
            return SSHTunnelForwarder(
                (self.connection_creds.get('ssh_host'), self.connection_creds.get('ssh_port')),
                ssh_username=self.connection_creds.get('ssh_username'),
                ssh_password=self.connection_creds.get('ssh_password'),
                ssh_private_key=self.connection_creds.get('ssh_private_key'),
                ssh_private_key_password=self.connection_creds.get('ssh_private_key_password'),
                remote_bind_address=(self.connection_creds.get('host'), self.connection_creds.get('port'))
            )

    def _create_in_database(self, character):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def _update_stats(self, character):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def add_character_with_user_id(self, character, user_id):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def add_all(self, characters_list):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def exist_by_id(self, character_id):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM characters WHERE id = %s", (character_id,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def find_all(self):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM characters')
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def find_all_by_playability_and_alive(self, playability, alive=True):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def find_all_by_playability_and_alive_and_level(self, playability, level, alive=True):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def find_all_by_user_id_and_alive(self, user_id, alive=True):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def find_by_id(self, character_id):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

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
