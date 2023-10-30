import psycopg2
from psycopg2 import extras
from repository.db_manager import DatabaseManager
from psycopg2.errors import InvalidTextRepresentation


class UserRepository:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def _create_in_database(self, name):
        connection = self.db_manager.get_connection()
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

    def _update_stats(self, user_id, name):
        connection = self.db_manager.get_connection()
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

    def exist_by_id(self, user_id):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s", (user_id,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
            connection.close()

    def find_all(self):
        connection = self.db_manager.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM users")
            records = cursor.fetchall()
            records_dict = [dict(record) for record in records]
            return records_dict
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, user_id):
        connection = self.db_manager.get_connection()
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

    def find_by_name(self, name):
        connection = self.db_manager.get_connection()
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
