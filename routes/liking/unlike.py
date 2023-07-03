"""
This module defines the route for unliking a post.

It includes a route for unliking a post in the Xonnet system.

Routes:
    - /post/unlike (POST): Unlike a post.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Like, Post, User, db

unlike_bp = Blueprint('unlike', __name__)

@unlike_bp.route('/post/unlike', methods=['POST'])
@jwt_required(refresh=True)
def unlike():
    """Unlike a post.

    This route is used to unlike a post in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - user_id: The ID of the user who liked the post.
        - post_id: The ID of the post to unlike.

    Returns:
        jsonify: A JSON response indicating the success or failure of the unlike operation.
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message": "User not found"}), 404

    data = request.json
    posts = Post.query.filter_by(user_id=data['user_id'])
    post_ids = [post.id for post in posts]

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"Message": "User not found"}), 404

    # Assign sequential IDs starting from 1 to each post
    post_id_mapping = {post_id: i + 1 for i, post_id in enumerate(post_ids)}

    if data['post_id'] not in post_id_mapping:
        # Post ID doesn't exist for the user
        return jsonify({"Message": "Post not found"}), 404

    like = Like.query.filter_by(user_id=user_id, post_id=data['post_id'], post_liked_of_id=data['user_id']).first()
    if not like:
        return jsonify({"Message": "Post not liked already"}), 400

    db.session.delete(like)
    db.session.commit()

    return jsonify({"Message": "Post unliked successfully"}), 200