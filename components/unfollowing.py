"""
This module defines a class and method for unfollowing a user.

Classes:
    - Unfollowing: A class for handling the unfollowing functionality.

Methods:
    - unfollowed_by(unfollower_id, unfollowed_id): Unfollow a user.

"""

from models import Follow, db

class Unfollowing:
    """
    A class for handling the unfollowing functionality.

    Methods:
        - unfollowed_by(unfollower_id, unfollowed_id): Unfollow a user.
    """

    def unfollowed_by(self, unfollower_id, unfollowed_id):
        """
        Unfollow a user.

        This method is used to unfollow a user by removing the follow relationship
        between the unfollower and the unfollowed user.

        Args:
            unfollower_id (int): The ID of the user who wants to unfollow.
            unfollowed_id (int): The ID of the user who is being unfollowed.

        Raises:
            Exception: If the unfollower is not following the unfollowed user.

        """
        try:
            follow = Follow.query.filter_by(follower_id=unfollower_id, followed_id=unfollowed_id).first()
            if not follow:
                raise Exception('You are not following this user.')

            db.session.delete(follow)
            db.session.commit()

        except Exception as e:
            raise e
