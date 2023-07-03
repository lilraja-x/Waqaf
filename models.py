"""
This module defines the database models for the application.

Classes:
    - User: Represents a user in the system.
    - Post: Represents a post made by a user.
    - Follow: Represents a follow relationship between users.
    - Like: Represents a like given by a user to a post.
    - Comment: Represents a comment made by a user on a post.

"""

import os
from time import time
from flask_sqlalchemy import SQLAlchemy
import datetime
import secrets
from sqlalchemy.ext.declarative import declarative_base
import jwt

db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database.

    This function initializes the SQLAlchemy database object with the Flask application.

    Args:
        app: The Flask application object.

    """
    db.init_app(app)


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        name (str): The name of the user.
        bio (str): The bio of the user.
        profile_image_url (str): The URL of the user's profile image.
        created_at (datetime): The timestamp of when the user account was created.
        updated_at (datetime): The timestamp of when the user account was last updated.
        posts (relationship): The posts made by the user.
        following (relationship): The users followed by the user.
        followers (relationship): The users following the user.
        likes (relationship): The likes given by the user.
        comments (relationship): The comments made by the user.

    """

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    bio = db.Column(db.String(100))
    profile_image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic')
    likes = db.relationship('Like', backref='liked_by', lazy=True)
    comments = db.relationship('Comment', backref='commented_by', lazy=True)

    def __init__(self, username, email, password, name, bio, profile_image_url):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.bio = bio
        self.profile_image_url = profile_image_url

    def get_reset_token(self, expires=3600):
        key = secrets.token_urlsafe(32)
        return jwt.encode({'reset_password': self.username,
                           'exp':    time() + expires},
                           key)

    def check(self, username, email, password):
        """
        Check user credentials.

        This method checks if the provided username and password match the user's credentials.

        Args:
            username (str): The username to check.
            email (str): The email address to check.
            password (str): The password to check.

        Returns:
            True if the credentials are valid.
            'Password incorrect!' if the password is incorrect.
            'No user found!' if no user with the provided username is found.

        """
        if username in self.username:
            if password == self.password:
                return True
            else:
                return 'Password incorrect!'
        else:
            return 'No user found!'


class Post(db.Model):
    """
    Represents a post made by a user.

    Attributes:
        id (int): The unique identifier of the post.
        user_id (int): The ID of the user who made the post.
        content (str): The content of the post.
        image_url (str): The URL of the image associated with the post.
        created_at (datetime): The timestamp of when the post was created.
        updated_at (datetime): The timestamp of when the post was last updated.
        likes (relationship): The likes received by the post.
        comments (relationship): The comments received by the post.

    """

    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    content = db.Column(db.String(100))
    image_url = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __init__(self, user_id, content, image_url):
        self.user_id = user_id
        self.content = content
        self.image_url = image_url


Base = declarative_base()

class Messaging(db.Model):
    """
    Represents a messaging relationship between users.

    Attributes:
        id (int): The unique identifier of the message.
        sender_id (int): The ID of the user who is sending the message.
        receiver_id (int): The ID of the user to whom the message is being sent.
        message (str): The content of the message.
        image_name (str): The name of the image file attached to the message.
        image_data (bytes): The binary data of the image file attached to the message.
        video_name (str): The name of the video file attached to the message.
        video_data (bytes): The binary data of the video file attached to the message.
        document_name (str): The name of the document file attached to the message.
        document_data (bytes): The binary data of the document file attached to the message.
        sent_at (datetime): The timestamp of when the message was sent.
        edited_at (datetime): The timestamp of when the message was last edited.
    """
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    message = db.Column(db.String(100))
    image_name = db.Column(db.String(100))
    image_data = db.Column(db.LargeBinary)
    video_name = db.Column(db.String(100))
    video_data = db.Column(db.LargeBinary)
    document_name = db.Column(db.String(100))
    document_data = db.Column(db.LargeBinary)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    edited_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, sender_id, receiver_id):
        self.sender_id = sender_id
        self.receiver_id = receiver_id

class Follow(db.Model):
    """
    Represents a follow relationship between users.

    Attributes:
        id (int): The unique identifier of the follow relationship.
        follower_id (int): The ID of the user who is following.
        followed_id (int): The ID of the user who is being followed.
        created_at (datetime): The timestamp of when the follow relationship was created.

    """

    __tablename__ = 'Follow'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id


class Like(db.Model):
    """
    Represents a like given by a user to a post.

    Attributes:
        id (int): The unique identifier of the like.
        user_id (int): The ID of the user who gave the like.
        post_id (int): The ID of the post that received the like.
        post_liked_of_id (int): The ID of the post that was liked.
        created_at (datetime): The timestamp of when the like was given.

    """

    __tablename__ = 'Likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)
    post_liked_of_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id, post_id, post_liked_of_id):
        self.user_id = user_id
        self.post_id = post_id
        self.post_liked_of_id = post_liked_of_id


class Comment(db.Model):
    """
    Represents a comment made by a user on a post.

    Attributes:
        id (int): The unique identifier of the comment.
        user_id (int): The ID of the user who made the comment.
        post_id (int): The ID of the post that received the comment.
        content (str): The content of the comment.
        post_commented_of_id (int): The ID of the post that was commented on.
        created_at (datetime): The timestamp of when the comment was made.

    """

    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False)
    content = db.Column(db.String(100))
    post_commented_of_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id, post_id, content, post_commented_of_id):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.post_commented_of_id = post_commented_of_id
