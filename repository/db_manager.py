from sshtunnel import SSHTunnelForwarder
import psycopg2.pool


class DatabaseManager:
    def __init__(self):
        self.connection_creds = {
            'name': 'global',
            'host': 'bandydan-3203.postgres.pythonanywhere-services.com',
            'port': 13203,
            'db_username': 'super',
            'db_password': 'U6Tdw8ReM',
            'db_name': 'charactersdb',
            'ssh_host': 'ssh.pythonanywhere.com',
            'ssh_port': 22,
            'ssh_username': 'bandydan',
            'ssh_password': 'xb6W7LHNJ6!cRKi',
            'ssh_private_key_password': 'masterkey',
            'ssh_private_key': '/home/vitaly/.ssh/id_rsa'
        }

        # self.connection_creds = {
        #     'name': 'local',
        #     'host': 'localhost',
        #     'db_name': 'charactersdb',
        #     'db_username': 'postgres',
        #     'db_password': 'admin'
        # }

        self.ssh_tunnel = None
        self._create_ssh_tunnel()

    def _create_ssh_tunnel(self):
        if self.connection_creds.get('name') == 'global':
            self.ssh_tunnel = SSHTunnelForwarder(
                (self.connection_creds.get('ssh_host'), self.connection_creds.get('ssh_port')),
                ssh_username=self.connection_creds.get('ssh_username'),
                ssh_password=self.connection_creds.get('ssh_password'),
                ssh_private_key=self.connection_creds.get('ssh_private_key'),
                ssh_private_key_password=self.connection_creds.get('ssh_private_key_password'),
                remote_bind_address=(self.connection_creds.get('host'), self.connection_creds.get('port'))
            )
            self.ssh_tunnel.start()
        else:
            self.ssh_tunnel = None

    def close_ssh_tunnel(self):
        if self.ssh_tunnel:
            self.ssh_tunnel.stop()
            self.ssh_tunnel = None

    def get_connection(self):
        if self.connection_creds.get('name') == 'global' and not self.ssh_tunnel:
            self._create_ssh_tunnel()
        if self.connection_creds.get('name') == 'local':
            return psycopg2.connect(
                        host=self.connection_creds.get('host'),
                        database=self.connection_creds.get('db_name'),
                        user=self.connection_creds.get('db_username'),
                        password=self.connection_creds.get('db_password')
                    )
        else:
            return psycopg2.connect(
                user=self.connection_creds.get('db_username'),
                password=self.connection_creds.get('db_password'),
                host='127.0.0.1',
                port=self.ssh_tunnel.local_bind_port,
                database=self.connection_creds.get('db_name'),
            )

