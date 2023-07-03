"""
This module defines a class and methods for posting and deleting posts.

Classes:
    - Posting: A class for handling the posting functionality.

Methods:
    - add_post(data): Add a new post.
    - delete_post(data): Delete a post.

"""

from models import Post, db

class Posting:
    """
    A class for handling the posting functionality.

    Methods:
        - add_post(data): Add a new post.
        - delete_post(data): Delete a post.
    """

    def add_post(self, data):
        """
        Add a new post.

        This method is used to create and add a new post to the database.

        Args:
            data (dict): A dictionary containing the post data, including 'user_id',
                         'content', and 'image'.

        Raises:
            Exception: If there is an error adding the post to the database.

        """
        try:
            post = Post(
                user_id=data['user_id'],
                content=data['content'],
                image_url=data['image'])
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            raise e

    def delete_post(self, data):
        """
        Delete a post.

        This method is used to delete a post from the database.

        Args:
            data (dict): A dictionary containing the post ID and user ID,
                         including 'post_id' and 'user_id'.

        Raises:
            ValueError: If the post is not found for the user.
            Exception: If there is an error deleting the post from the database.

        """
        try:
            post = Post.query.filter_by(id=data['post_id'], user_id=data['user_id']).first()
            if post:
                db.session.delete(post)
                db.session.commit()
            else:
                raise ValueError("Post not found for the user")
        except Exception as e:
            raise e
