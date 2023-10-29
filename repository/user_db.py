import psycopg2
from psycopg2 import extras
from sshtunnel import SSHTunnelForwarder
from psycopg2.errors import InvalidTextRepresentation


class UserRepository:
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

    def _create_in_database(self, name):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name)"
                "VALUES (%s) RETURNING id",
                (name,)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            return new_id
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def _update_stats(self, user_id, name):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE users SET name = %s WHERE id = %s",
                (name, user_id)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def exist_by_id(self, user_id):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", (user_id,))
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
            cursor.execute("SELECT * FROM users")
            records = cursor.fetchall()
            records_dict = [dict(record) for record in records]
            return records_dict
        finally:
            cursor.close()
            connection.close()
            if tunnel is not None:
                tunnel.stop()

    def find_by_id(self, user_id):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
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

    def find_by_name(self, name):
        tunnel = self._create_tunnel()
        if tunnel is not None:
            tunnel.start()
        connection = self._create_connection(tunnel)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
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

    def add_user(self, name):
        if self.find_by_name(name) is None:
            new_id = self._create_in_database(name)
            return new_id
        else:
            raise ValueError

    def update_mob(self, user_id, name):
        if self.exist_by_id(user_id):
            self._update_stats(user_id, name)
            return True
        else:
            return False
