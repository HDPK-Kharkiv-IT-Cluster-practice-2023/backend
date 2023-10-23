import psycopg2
from sshtunnel import SSHTunnelForwarder


def create_ssh_tunnel():
    ssh_host = 'ssh.pythonanywhere.com'
    ssh_port = 22
    ssh_username = 'bandydan'
    ssh_password = 'xb6W7LHNJ6!cRKi'

    ssh_private_key_password = 'masterkey'
    ssh_private_key = '/home/vitaly/.ssh/id_rsa'

    return SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        ssh_private_key=ssh_private_key,
        ssh_private_key_password=ssh_private_key_password,
        remote_bind_address=('bandydan-3203.postgres.pythonanywhere-services.com', 13203)
    )


def create_database_connection(tunnel):
    return psycopg2.connect(
        user='super',
        password='U6Tdw8ReM',
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        database='charactersdb',
    )
