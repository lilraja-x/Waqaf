"""
This module defines a class and methods for user creation.

Classes:
    - Create: A class for creating user accounts.

Methods:
    - create_account(data, bcrypt): Create a user account.

"""

from models import User, db
from flask import current_app


class Create:
    """
    A class for creating user accounts.

    Methods:
        - create_account(data, bcrypt): Create a user account.

    """

    def create_account(self, data, bcrypt):
        """
        Create a user account.

        This method is used to create a new user account with the provided data.

        Args:
            data (dict): Contains all the information of the user.
            bcrypt: The bcrypt object used for password hashing.

        Raises:
            Exception: If there is an error during the account creation process.

        """
        try:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            account = User(
                username=data['username'],
                email=data['email'],
                password=hashed_password,
                profile_image_url=data['profile_image_url'],
                name=data['name'],
                bio=data['bio']
            )
            db.session.add(account)
            db.session.commit()
        except Exception as e:
            raise e

