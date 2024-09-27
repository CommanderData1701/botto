import sqlite3
import unittest

from ..database import Database
from ..user import User


class TestDatabase(unittest.TestCase):

    def test_database_create_user(self):
        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        db = Database(connection)

        user_objects = list()

        user_objects.append(db.create_user("John Doe"))
        user_objects.append(db.create_user("Jane Doe", is_admin=True))

        cursor.execute('SELECT name, chat_id, token, is_admin FROM users')
        users = cursor.fetchall()

        self.assertTrue(len(users) == 2)
        self.assertTrue(("John Doe", None, users[0][2], 0) in users)
        self.assertTrue(("Jane Doe", None, users[1][2], 1) in users)
        self.assertTrue(all(len(token) == 6 for _, _, token, _ in users))
        self.assertTrue(all(token.isalnum() and token == token.lower() for _, _, token, _ in users))

        user = user_objects[0]
        self.assertEqual(user.name, "John Doe")
        self.assertIsNone(user.chat_id)
        self.assertEqual(user.is_admin, False)

        user = user_objects[1]
        self.assertEqual(user.name, "Jane Doe")
        self.assertIsNone(user.chat_id)
        self.assertEqual(user.is_admin, True)

    def test_get_users(self):
        connection = sqlite3.connect(':memory:')
        db = Database(connection)

        db.create_user(name="John Doe", chat_id=43)
        db.create_user(name="Jane Doe", is_admin=True)

        users = db.get_users()

        self.assertTrue(len(users) == 2)
        self.assertTrue(all(isinstance(user, User) for user in users))
        self.assertTrue(users[0].name == "John Doe")
        self.assertTrue(users[0].is_admin == False)
        self.assertTrue(users[0].chat_id == 43)
        self.assertTrue(users[1].name == "Jane Doe")
        self.assertTrue(users[1].is_admin == True)
        self.assertIsNone(users[1].chat_id)


if __name__ == "__main__":
    unittest.main()
