# -*- coding: utf-8 -*-
"""Module containing the database class."""
import sqlite3
from random import choice
from typing import Optional

from .user import User


class Database:
    """Class representing the database.

    Class representation of the database connection. Database is implemented
    using sqlite3.

    Attributes:
        connection (sqlite3.Connection): The connection to the database.
        cursor (sqlite3.Cursor): The cursor for the database connection.
    """
    def __init__(
        self, mock_connection: Optional[sqlite3.Connection] = None
    ) -> None:
        if mock_connection:
            self.connection = mock_connection
        else:
            self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        self.create_tables()

    @staticmethod
    def generate_token() -> str:
        """Generates a six digit token made of alphanumeric characters."""
        return ''.join(
            [choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(6)]
        )

    def __del__(self) -> None:
        """Closes the database connection."""
        self.connection.close()

    def create_tables(self) -> None:
        """Creates the tables in the database if they do not exist."""
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
        """Creates a new user in the database.

        Parameters:
        """
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
        """Updates user in the database.

        Parameters:
            old_user (User): User to be updated.
            new_user (User): User with updated information.

        Returns:
            User: The old user object.

        Todo:
            * Add handling for when the user is not found.
        """
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
        """Method for just updateing the name of a user.
        
        Parameters:
            old_name (str): The old name of the user.
            new_name (str): The new name of the use
                
        Todo:
            * Add handling for when the user is not found
        """
        self.cursor.execute(
            'UPDATE users SET name = ? WHERE name = ?', (new_name, old_name)
        )
        self.connection.commit()

    def set_user_chat_id(self, user: User, chat_id: int) -> None:
        """Update chat id of a user in the database.

        Parameters:
            user (User): The user to update.
            chat_id (int): The chat id to set.

        Todo:
            * Add handling for when the user is not found.
        """
        self.cursor.execute(
            'UPDATE users SET chat_id = ? WHERE name = ?', (chat_id, user.name))
        self.connection.commit()

    def get_users(self) -> list[User]:
        """Returns a list of all users in the database.

        Returns:
            list[User]: A list of all users in the database
        """
        self.cursor.execute('SELECT chat_id, name, token, is_admin FROM users')
        users = self.cursor.fetchall()

        return [
            User(chat_id=chat_id, name=name, token=token, is_admin=is_admin)
            for chat_id, name, token, is_admin in users
        ]

    def get_user_by_name(self, name: str) -> Optional[User]:
        """Returns a user by name.

        Parameters:
            name (str): The name of the user to return.
        
        Returns:
            Optional[User]: The user with the given name or None if the user is
                not found.
        """
        self.cursor.execute(
            'SELECT chat_id, name, token, is_admin FROM users WHERE name = ?',
            (name,)
        )
        user = self.cursor.fetchone()

        return User(chat_id=user[0], name=user[1], token=user[2],
                    is_admin=user[3]==1) if user else None
    
    def get_user_by_chat_id(self, chat_id: int) -> Optional[User]:
        """Returns a user by chat id.

        Parameters:
            chat_id (int): The chat id of the user to return.

        Returns:
            Optional[User]: The user with the given chat id or None if the user
                is not found.
        """
        self.cursor.execute(
            'SELECT chat_id, name, token, is_admin FROM users WHERE chat_id = ?',
            (chat_id,)
        )
        user = self.cursor.fetchone()

        return User(chat_id=user[0], name=user[1], token=user[2],
                    is_admin=user[3]==1) if user else None
