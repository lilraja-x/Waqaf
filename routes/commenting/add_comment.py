"""
This module defines the route for adding a comment.

It includes a route for adding a comment to a post in the Xonnet system.

Routes:
    - /comment/add (POST): Add a comment to a post.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Comment, Post, User, db

add_comment_bp = Blueprint('add_comment', __name__)

@add_comment_bp.route('/comment/add', methods=['POST'])
@jwt_required(refresh=True)
def add_comment():
    """Add a comment to a post.

    This route is used to add a comment to a post in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - user_id: The ID of the user adding the comment.
        - post_id: The ID of the post the comment will be added to.
        - content: The content of the comment to be added.

    Returns:
        jsonify: A JSON response indicating the success or failure of the comment addition operation.
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

    comment = Comment(user_id=user_id, post_id=data['post_id'], post_commented_of_id=data['user_id'], content=data['content'])
    try:
        db.session.add(comment)
        db.session.commit()
        return jsonify({"Message": "Comment added successfully"}), 200
    except Exception as e:
        return jsonify({"Message": "Failed to add comment!", "Error": str(e)}), 400