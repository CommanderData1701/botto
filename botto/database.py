import sqlite3
from random import choice
from typing import Optional

from .user import User


class Database:
    def __init__(self, mock_connection=None) -> None:
        if mock_connection:
            self.connection = mock_connection
        else:
            self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        self.create_tables()

    @staticmethod
    def generate_token():
        return ''.join(
            [choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(6)]
        )

    def __del__(self) -> None:
        self.connection.close()

    def create_tables(self) -> None:
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

    def create_user(
        self,
        name: str,
        chat_id: Optional[int] = None,
        is_admin: bool = False
    ) -> User:
        token = Database.generate_token()
        self.cursor.execute('''
            INSERT INTO users (chat_id, name, is_admin, token)
            VALUES (?, ?, ?, ?)
        ''', (chat_id, name, is_admin, token))
        self.connection.commit()

        return User(
            token=token, chat_id=chat_id, name=name, is_admin=is_admin == 1
        )

    def update_user(self, old_user: User, new_user: User) -> User:
        self.cursor.execute(
            '''
            UPDATE users
            SET chat_id = ?, name = ?, is_admin = ?
            WHERE name = ?
            ''', 
            (new_user.chat_id, new_user.name, new_user.is_admin, old_user.name)
        )
        self.connection.commit()

        return old_user

    def update_user_name(self, old_name: str, new_name: str) -> None:
        self.cursor.execute(
            'UPDATE users SET name = ? WHERE name = ?', (new_name, old_name)
        )
        self.connection.commit()

    def set_user_chat_id(self, user: User, chat_id: int) -> None:
        self.cursor.execute(
            'UPDATE users SET chat_id = ? WHERE name = ?', (chat_id, user.name))
        self.connection.commit()

    def get_users(self) -> list[User]:
        self.cursor.execute('SELECT chat_id, name, token, is_admin FROM users')
        users = self.cursor.fetchall()

        return [
            User(chat_id=chat_id, name=name, token=token, is_admin=is_admin)
            for chat_id, name, token, is_admin in users
        ]

    def get_user_by_name(self, name: str) -> Optional[User]:
        self.cursor.execute(
            'SELECT chat_id, name, token, is_admin FROM users WHERE name = ?',
            (name,)
        )
        user = self.cursor.fetchone()

        return User(chat_id=user[0], name=user[1], token=user[2], 
                    is_admin=user[3]==1) if user else None
