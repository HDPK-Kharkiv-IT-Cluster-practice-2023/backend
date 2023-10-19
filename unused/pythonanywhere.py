import psycopg2
from sshtunnel import SSHTunnelForwarder

host = 'bandydan-3203.postgres.pythonanywhere-services.com'
port = 13203
db_username = 'super'
db_password = 'U6Tdw8ReM'
database_name = 'charactersdb' #Write the database name here

# SSH tunnel configuration
ssh_host = 'ssh.pythonanywhere.com'  # Replace with your SSH host
ssh_port = 22  # Replace with your SSH port
ssh_username = 'bandydan'  # Replace with your SSH username
ssh_password = 'xb6W7LHNJ6!cRKi'  # Replace with your SSH password

ssh_private_key_password = 'masterkey'
ssh_private_key = '/home/vitaly/.ssh/id_rsa'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        ssh_private_key=ssh_private_key,
        ssh_private_key_password=ssh_private_key_password,
        remote_bind_address=(host, port)
) as tunnel:
    # Establish a connection to the target database
    connection = psycopg2.connect(
        user=db_username,
        password=db_password,
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        database=database_name,
    )

    cursor = connection.cursor()
    table_name = 'characters' #Write the table name here
    query = f'SELECT * FROM {table_name};'
    cursor.execute(query)

    # Fetch the data from the table
    rows = cursor.fetchall()

    # Iterate through the rows and print the data
    for row in rows:
        print(row)

    # Close the cursor and the connection
    cursor.close()
    connection.close()