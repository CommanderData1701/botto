import sqlite3
from random import choice

from .user import User


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chat_id INTEGER,
            token TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS shopping_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            added_by INTEGER NOT NULL,
            FOREIGN KEY (added_by) REFERENCES users(user_id)
        )''')

        self.connection.commit()

    def create_user(self, name: str, chat_id: int = None, is_admin: bool = False) -> None:
        self.cursor.execute('''
            INSERT INTO users (chat_id, name, is_admin, token)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, name, is_admin, self.generate_token()))
        self.connection.commit()

        return User(chat_id=chat_id, name=name, is_admin=is_admin)

    def update_user(self, old_user: User, new_user: User) -> None:
        self.cursor.execute('''
            UPDATE users
            SET chat_id = ?, name = ?, is_admin = ?
            WHERE name = ?
        ''', (new_user.chat_id, new_user.name, new_user.is_admin, old_user.name))
        self.connection.commit()

    def set_user_chat_id(self, user: User, chat_id: int) -> None:
        self.cursor.execute('UPDATE users SET chat_id = ? WHERE name = ?', (chat_id, user.name))
        self.connection.commit()

    def get_users(self) -> list[User]:
        self.cursor.execute('SELECT chat_id, name, token, is_admin FROM users')
        users = self.cursor.fetchall()

        return [
            User(chat_id, name, token, is_admin) for chat_id, name, token, is_admin in users
        ]

    def generate_token(self):
        return ''.join([choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(6)])
