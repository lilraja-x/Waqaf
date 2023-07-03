"""
This module defines a class and methods for user login.

Classes:
    - Login: A class for handling the login functionality.

Methods:
    - check(data): Check user credentials and generate access and refresh tokens.

"""

from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from models import User


class Login:
    """
    A class for handling the login functionality.

    Methods:
        - check(data): Check user credentials and generate access and refresh tokens.
    """

    def check(self, data):
        """
        Check user credentials and generate access and refresh tokens.

        This method is used to validate user credentials and generate access and refresh tokens
        for authenticated users.

        Args:
            data (dict): A dictionary containing the user login data, including 'username' and 'password'.

        Returns:
            tuple: A tuple containing the access token, username, user ID, and refresh token.

        Raises:
            Exception: If the provided credentials are invalid or incorrect.

        """
        try:
            bcrypt = current_app.config['bcrypt']
            user = User.query.filter_by(username=data['username']).first()
            if user:
                is_valid = bcrypt.check_password_hash(user.password, data['password'])
                if is_valid:
                    access_token = create_access_token(identity=user.id)
                    refresh_token = create_refresh_token(identity=user.id)
                    return access_token, user.username, user.id, refresh_token
            raise Exception('Invalid credentials!')
        except:
            raise Exception('Username or Password is not correct!')