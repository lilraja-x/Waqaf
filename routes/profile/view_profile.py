"""
This module defines the routes related to user profiles.

It includes routes for retrieving user profile information such as username, name, profile image, bio, email,
post count, followers count, following count, likes count, and comments count.

Routes:
    - /profile/view (GET): Retrieve user profile information.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Comment, Like, User, db

view_profile_bp = Blueprint('view_profile', __name__)

@view_profile_bp.route('/profile/view', methods=['GET'])
@jwt_required(refresh=True)
def view_profile():
    """Retrieve user profile information.

    This route is used to retrieve detailed information about a user's profile.
    It includes the user's username, name, profile image URL, bio, email,
    creation timestamp, last update timestamp, post count, list of posts with their details,
    followers count, list of followers, following count, list of users being followed,
    likes count, and comments count.

    Returns:
        jsonify: A JSON response containing the user's profile information.
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"Message": "User not found"}), 404

    try:
        posts = [{
            "id": post.id,
            "content": post.content,
            "image": post.image_url
        } for post in user.posts]

        followers = [{
            "id": follower.id
        } for follower in user.followers]

        following = [{
            "id": follow.followed_id
        } for follow in user.following]

        likes_count = Like.query.filter_by(user_id=user.id).count()
        comments_count = Comment.query.filter_by(user_id=user.id).count()

        return jsonify({
            "Message": "Data fetched!",
            "Username": user.username,
            "Name": user.name,
            "Profile Image": user.profile_image_url,
            "Bio": user.bio,
            "Email": user.email,
            "Created At": user.created_at,
            "Last Updated At": user.updated_at,
            "Posts Count": len(user.posts),
            "Posts": posts,
            "Followers Count": user.followers.count(),
            "Followers": followers,
            "Following Count": user.following.count(),
            "Following": following,
            "Likes Count": likes_count,
            "Comments Count": comments_count
        })

    except:
        return jsonify({"Message": "Failed to view profile!", "Error": str(Exception)}), 400