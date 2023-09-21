import psycopg2


class CharacterRepository:
    def __init__(self, character):
        self.character = character
        self.connection_creds = {
            'host': 'localhost',
            'database': 'charactersdb',
            'user': 'postgres',
            'password': 'admin'
        }
        # Создать персонажа в базе данных
        self.create_in_database()

    def create_in_database(self):
        connection = psycopg2.connect(
            host=self.connection_creds.get('host'),
            database=self.connection_creds.get('database'),
            user=self.connection_creds.get('user'),
            password=self.connection_creds.get('password')
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO characters (name, critical_attack, health, armor, attack, luck)"
            " VALUES (%s, %s, %s, %s, %s, %s)",
            (self.character.name, self.character.critical_attack, self.character.health, self.character.armor,
             self.character.attack, self.character.luck)
        )
        connection.commit()
        cursor.close()
        connection.close()

    def update_stats(self):
        connection = psycopg2.connect(
            host=self.connection_creds.get('host'),
            database=self.connection_creds.get('database'),
            user=self.connection_creds.get('user'),
            password=self.connection_creds.get('password')
        )
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE characters SET critical_attack = %s, health = %s, armor = %s,"
            " attack = %s, luck = %s WHERE name = %s",
            (self.character.critical_attack, self.character.health, self.character.armor, self.character.attack,
             self.character.luck, self.character.name)
        )
        connection.commit()
        cursor.close()
        connection.close()

    def find_all(self):
        connection = psycopg2.connect(
            host=self.connection_creds.get('host'),
            database=self.connection_creds.get('database'),
            user=self.connection_creds.get('user'),
            password=self.connection_creds.get('password')
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM characters")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records

    def find_by_id(self, character_id):
        connection = psycopg2.connect(
            host=self.connection_creds.get('host'),
            database=self.connection_creds.get('database'),
            user=self.connection_creds.get('user'),
            password=self.connection_creds.get('password')
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM characters WHERE id = %s", (character_id,))
        record = cursor.fetchone()
        cursor.close()
        connection.close()
        return record

    def update_character(self, character):
        self.character = character
        self.update_stats()

    def __str__(self):
        return (f"{self.character.name}: критическая атака {self.character.critical_attack},"
                f" здоровье {self.character.health}, броня {self.character.armor}, атака {self.character.attack},"
                f" удача {self.character.luck}")


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
