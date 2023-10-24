from database import create_ssh_tunnel, initialize_character, load_character_data, load_items_from_database
from shop import main

if __name__ == "__main__":
    char_id = 1  # Replace character's personal ID
    db_username = 'super'
    db_password = 'U6Tdw8ReM'
    tunnel = create_ssh_tunnel()
    tunnel.start()
    character_database_name = 'charactersdb'
    items_database_name = 'item_database'

    initialize_character(char_id, db_username, db_password, tunnel, character_database_name)
    balance, inventory = load_character_data(char_id, db_username, db_password, tunnel, character_database_name)
    items = load_items_from_database(db_username, db_password, tunnel, items_database_name)

    main(char_id, db_username, db_password, tunnel, character_database_name, balance, inventory, items)
