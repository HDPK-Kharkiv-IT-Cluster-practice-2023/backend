import psycopg2
from psycopg2 import extras
from sshtunnel import SSHTunnelForwarder


class MobRepository:
    def __init__(self):
        self.connection_creds = {
            'host': 'bandydan-3203.postgres.pythonanywhere-services.com',
            'port': 13203,
            'db_username': 'super',
            'db_password': 'U6Tdw8ReM',
            'database_name': 'charactersdb',
            'ssh_host': 'ssh.pythonanywhere.com',
            'ssh_port': 22,
            'ssh_username': 'bandydan',
            'ssh_password': 'xb6W7LHNJ6!cRKi',
            'ssh_private_key_password': 'masterkey',
            'ssh_private_key': '/home/vitaly/.ssh/id_rsa'
        }

        # local database

        # self.connection_creds = {
        #     'host': 'localhost',
        #     'database': 'charactersdb',
        #     'user': 'postgres',
        #     'password': 'admin'
        # }

    # local database

    # def _create_connection(self, tunnel):
    #     # return psycopg2.connect(
    #     #     host=self.connection_creds.get('host'),
    #     #     database=self.connection_creds.get('database'),
    #     #     user=self.connection_creds.get('user'),
    #     #     password=self.connection_creds.get('password')
    #     # )

    # def _create_tunnel(self):
    #     return None

    def _create_tunnel(self):
        return SSHTunnelForwarder(
            (self.connection_creds.get('ssh_host'), self.connection_creds.get('ssh_port')),
            ssh_username=self.connection_creds.get('ssh_username'),
            ssh_password=self.connection_creds.get('ssh_password'),
            ssh_private_key=self.connection_creds.get('ssh_private_key'),
            ssh_private_key_password=self.connection_creds.get('ssh_private_key_password'),
            remote_bind_address=(self.connection_creds.get('host'), self.connection_creds.get('port'))
        )

    def _create_connection(self, tunnel):
        connection = psycopg2.connect(
            user=self.connection_creds.get('db_username'),
            password=self.connection_creds.get('db_password'),
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            database=self.connection_creds.get('database_name'),
        )
        return connection

    def _create_in_database(self, character):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def _update_stats(self, character):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def add_all(self, characters_list):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def exist_by_id(self, character_id):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM mob_types WHERE id = %s", (character_id,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def find_all(self):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM mob_types")
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def find_all_by_alive(self, alive=True):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM mob_types "
                           "WHERE alive = %s ", (alive,))
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def find_all_by_alive_and_level(self, level, alive=True):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
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
            if tunnel is not None:
                tunnel.stop()

    def find_by_id(self, character_id):
        tunnel = self._create_tunnel()
        tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM mob_types WHERE id = %s", (character_id,))
            record = cursor.fetchone()
            return record
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def add_mob(self, character):
        if character.id is None:
            new_id = self._create_in_database(character)
            character.id = new_id
            return True
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
