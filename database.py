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


def initialize_character(char_id, db_username, db_password, tunnel, database_name):
    with psycopg2.connect(
            user=db_username,
            password=db_password,
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            database=database_name,
    ) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT id FROM characters WHERE id = %s;', (char_id,))
        existing_character = cursor.fetchone()

        if existing_character:
            query = 'UPDATE characters SET owner = %s, status = %s, balance = %s, inventory = %s WHERE id = %s;'
            initial_inventory = []
            cursor.execute(query, ('default_owner', 'default_status', 0, initial_inventory, char_id))
        else:
            query = 'INSERT INTO characters (id, owner, status, balance, inventory) VALUES (%s, %s, %s, %s, %s);'
            initial_inventory = []
            cursor.execute(query, (char_id, 'default_owner', 'default_status', 0, initial_inventory))

        connection.commit()


def load_character_data(char_id, db_username, db_password, tunnel, database_name):
    with psycopg2.connect(
            user=db_username,
            password=db_password,
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            database=database_name,
    ) as connection:
        cursor = connection.cursor()

        query = 'SELECT balance, inventory FROM characters WHERE id = %s;'
        cursor.execute(query, (char_id,))
        result = cursor.fetchone()

        balance = 0
        inventory = []

        if result:
            balance = result[0]
            inventory = result[1] if result[1] else []

        return balance, inventory


def load_items_from_database(db_username, db_password, tunnel, database_name):
    items = {}
    with psycopg2.connect(
            user=db_username,
            password=db_password,
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            database=database_name,
    ) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT name, price, category, details FROM items;")
        rows = cursor.fetchall()

        for row in rows:
            name, price, category, details = row
            items[name] = {
                'price': price,
                'category': category,
                'details': details
            }

    return items
