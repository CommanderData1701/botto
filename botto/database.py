"""
This module contains the Database class, which is responsible for managing the
database connection and the user data.

Classes:
--------
Database:
    Class that manages the database connection and user data.
"""

import sqlite3
from random import choice
from typing import Optional

from .user import User


class Database:
    """
    Class that manages the database connection and user data.

    Attributes:
    ----------
    connection : sqlite3.Connection
        The connection to the database.

    cursor : sqlite3.Cursor
        The cursor to the database.

    Methods:
    --------
    generate_token(): (staticmethod)
        Generates a random token for the user.

    __del__():
        Closes the connection to the database.

    create_tables():
        Creates the tables in the database if they do not exist.

    create_user(
        name: str, chat_id: Optional[int] = None, is_admin: bool = False
    ) -> User:
        Creates a new user in the database.

    update_user(old_user: User, new_user: User) -> User:
        Updates the user in the database.

    update_user_name(old_name: str, new_name: str) -> None:
        Updates the user's name in the database.

    set_user_chat_id(user: User, chat_id: int) -> None:
        Sets the chat id of the user in the database.

    get_users() -> list[User]:
        Gets all the users from the database.

    get_user_by_name(name: str) -> Optional[User]:
        Gets a user by their name from the database.
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
        """
        Generates a random token of lenght 6 for the user.
        """
        return ''.join(
            [choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(6)]
        )

    def __del__(self) -> None:
        self.connection.close()

    def create_tables(self) -> None:
        """
        Creates the tables in the database if they do not exist
        """
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
        """
        Creates a new user in the database.

        Parameters:
        -----------
        name : str
            The name of the user.

        chat_id : Optional[int]
            The chat id of the user.

        is_admin : bool
            Whether the user is an admin or not.

        Returns:
        --------
        User
            The user object created.
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
        """
        Updates the user in the database.

        Parameters:
        -----------
        old_user : User
            The old user object.

        new_user : User
            The new user object.

        Returns:
        --------
        User
            The old user object.
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
        """
        Updates the user's name in the database.

        Parameters:
        -----------
        old_name : str
            The old name of the user.

        new_name : str
            The new name of the use
        """
        self.cursor.execute(
            'UPDATE users SET name = ? WHERE name = ?', (new_name, old_name)
        )
        self.connection.commit()

    def set_user_chat_id(self, user: User, chat_id: int) -> None:
        """
        Sets the chat id of the user in the database.

        Parameters:
        -----------
        user : User
            The user object.

        chat_id : int
            The chat id of the user.
        """
        self.cursor.execute(
            'UPDATE users SET chat_id = ? WHERE name = ?', (chat_id, user.name))
        self.connection.commit()

    def get_users(self) -> list[User]:
        """
        Gets all the users from the database.

        Returns:
        --------
        list[User]
            The list of users in the database.
        """
        self.cursor.execute('SELECT chat_id, name, token, is_admin FROM users')
        users = self.cursor.fetchall()

        return [
            User(chat_id=chat_id, name=name, token=token, is_admin=is_admin)
            for chat_id, name, token, is_admin in users
        ]

    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Gets a user by their name from the database.

        Parameters:
        -----------
        name : str
            The name of the user.

        Returns:
        --------
        Optional[User]
            The user object if found, else None.
        """
        self.cursor.execute(
            'SELECT chat_id, name, token, is_admin FROM users WHERE name = ?',
            (name,)
        )
        user = self.cursor.fetchone()

        return User(chat_id=user[0], name=user[1], token=user[2],
                    is_admin=user[3]==1) if user else None
