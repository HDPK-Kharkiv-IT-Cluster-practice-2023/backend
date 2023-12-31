import json
from ssh_tunnel import create_database_connection


class Shop:
    def __init__(self, initial_money, char_id, tunnel):
        self.money = initial_money
        self.character_id = char_id
        self.inventory = []

        self.melee_weapons = {
            "Sword of Dragons": {'price': 50, 'damage': 10, 'effect': 'poison'}
        }

        self.ranged_weapons = {
            "Blood Eye Bow": {'price': 100, 'damage': 20, 'effect': 'poison'}
        }

        self.items = {
            'Iron Armor': {'price': 150, 'armor': 20},
            'Health Potion': {'price': 30, 'health': 50},
            'Lucky Amulet': {'price': 50, 'luck': 0.1},
            'Crit Dagger': {'price': 100, 'critical_damage': 0.5}
        }
        self.legendary_items = {
            'Excalibur': {'price': 1000, 'damage': 100, 'effect': 'holy smite'}
        }

        self.tunnel = tunnel

        self.initialize_character(char_id)
        self.load_character_data()

    def initialize_character(self, char_id):
        with create_database_connection(self.tunnel) as connection:
            cursor = connection.cursor()

            query = 'SELECT COUNT(*) FROM characters WHERE id = %s;'
            cursor.execute(query, (char_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                query = 'INSERT INTO characters (id, balance, inventory) VALUES (%s, %s, %s);'
                initial_inventory = []
                cursor.execute(query, (char_id, 0, initial_inventory))
                connection.commit()

    def load_character_data(self):
        with create_database_connection(self.tunnel) as connection:
            cursor = connection.cursor()

            query = 'SELECT balance, inventory FROM characters WHERE id = %s;'
            cursor.execute(query, (self.character_id,))
            result = cursor.fetchone()

            if result:
                self.money = result[0]
                self.inventory = result[1] if result[1] else []
            else:
                self.money = 0
                self.inventory = []

    def save_character_data(self):
        with create_database_connection(self.tunnel) as connection:
            cursor = connection.cursor()

            query = 'UPDATE characters SET balance = %s, inventory = %s WHERE id = %s;'
            inventory_json = json.dumps(self.inventory)
            cursor.execute(query, (self.money, inventory_json, self.character_id))
            connection.commit()

    def show_category(self, category_name, items):
        print(f'Available {category_name}:')
        for i, (item, details) in enumerate(items.items(), start=1):
            print(f'{i}. {item}: Price - {details["price"]} UAH, '
                  f'{", ".join([f"{k}: {v}" for k, v in details.items() if k != "price"])}')
        print(f'Your balance: {self.money} UAH')

    def show_weapons(self):
        self.show_category("weapons", {**self.melee_weapons, **self.ranged_weapons})

    def show_items(self):
        self.show_category("items", self.items)

    def show_legendary_items(self):
        self.show_category("legendary items", self.legendary_items)

    def purchase_item(self, item_name, item_price):
        if self.money >= item_price:
            self.inventory.append(item_name)

            self.money -= item_price
            self.save_character_data()
            return True
        else:
            return False
