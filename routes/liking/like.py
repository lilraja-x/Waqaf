"""
This module defines the route for liking a post.

It includes a route for liking a post in the Xonnet system.

Routes:
    - /post/like (POST): Like a post.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Like, Post, User, db

like_bp = Blueprint('like', __name__)

@like_bp.route('/post/like', methods=['POST'])
@jwt_required(refresh=True)
def like():
    """Like a post.

    This route is used to like a post in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - user_id: The ID of the user performing the like.
        - post_id: The ID of the post to like.

    Returns:
        jsonify: A JSON response indicating the success or failure of the like operation.
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

    # Assign sequential IDs starting from 1 to each post
    post_id_mapping = {post_id: i + 1 for i, post_id in enumerate(post_ids)}
    
    if data['post_id'] not in post_id_mapping.values():
        # Post ID doesn't exist for the user
        return jsonify({"Message": "Post not found"}), 404
    
    like = Like.query.filter_by(user_id=user_id, post_id=data['post_id'], post_liked_of_id=data['user_id']).first()
    if like:
        return jsonify({"Message": "Post liked already"}), 400
    
    like = Like(user_id=user_id, post_id=data['post_id'], post_liked_of_id=data['user_id'])
    db.session.add(like)
    db.session.commit()
    return jsonify({"Message": "Post liked successfully"}), 200