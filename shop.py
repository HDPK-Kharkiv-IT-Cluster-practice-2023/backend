import json
import psycopg2


def purchase_item(item_name, item_price, balance, inventory, char_id, db_username, db_password, tunnel,
                  character_database_name):
    if balance >= item_price:
        balance -= item_price
        inventory.append(item_name)

        inventory_json = json.dumps(inventory)

        with psycopg2.connect(
                user=db_username,
                password=db_password,
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                database=character_database_name,
        ) as connection:
            cursor = connection.cursor()
            query = 'UPDATE characters SET balance = %s, inventory = %s::jsonb WHERE id = %s;'
            cursor.execute(query, (balance, inventory_json, char_id))
            connection.commit()

        return balance, inventory
    else:
        return balance, inventory


def main(char_id, db_username, db_password, tunnel, character_database_name, balance, inventory, items):
    print(f"Your balance: {balance} UAH")

    while True:
        print("List of available items:")
        for index, (item_name, item_data) in enumerate(items.items(), start=1):
            category = item_data['category']
            price = item_data['price']
            details = item_data['details']
            print(f"{index}. Name: {item_name}, Category: {category}, Price: {price} UAH, Details: {details}")

        print("0. Exit")
        choice = input("Enter the item number you want to purchase, or 0 to exit: ")

        if choice == "0":
            break

        try:
            choice = int(choice)
            if choice < 1 or choice > len(items):
                raise ValueError

            item_name = list(items.keys())[choice - 1]
            item_price = items[item_name]['price']

            balance, inventory = purchase_item(item_name, item_price, balance, inventory, char_id, db_username,
                                               db_password, tunnel, character_database_name)
            if balance >= 0:
                print(f'You bought {item_name} for {item_price} UAH. Remaining balance: {balance} UAH')
            else:
                print('Failed to buy the item. Insufficient funds.')

        except ValueError:
            print('Invalid input. Please enter a valid number or 0 to exit.')

