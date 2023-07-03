"""
This module defines a class and methods for user following.

Classes:
    - Following: A class for handling the user following functionality.

Methods:
    - followed_by(follower_id, followed_id): Follow a user.
    - followed_to(data): Get the ID of a user based on the username.

"""

from models import Follow, db, User


class Following:
    """
    A class for handling the user following functionality.

    Methods:
        - followed_by(follower_id, followed_id): Follow a user.
        - followed_to(data): Get the ID of a user based on the username.

    """

    def followed_by(self, follower_id, followed_id):
        """
        Follow a user.

        This method is used to make a user follow another user.

        Args:
            follower_id (int): The ID of the user who wants to follow.
            followed_id (int): The ID of the user being followed.

        Raises:
            Exception: If the user is already following the specified user.

        """
        try:
            follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
            if follow:
                raise Exception('Already followed this user.')

            follow = Follow(
                follower_id=follower_id,
                followed_id=followed_id
            )
            db.session.add(follow)
            db.session.commit()
        except Exception as e:
            raise e

    def followed_to(self, data):
        """
        Get the ID of a user based on the username.

        This method is used to retrieve the ID of a user based on their username.

        Args:
            data (str): The username of the user.

        Returns:
            int: The ID of the user.

        Raises:
            Exception: If the specified username is not found.

        """
        try:
            user = User.query.filter_by(username=data).first()
            if user.username:
                return user.id
        except:
            raise Exception('Username not correct!')
