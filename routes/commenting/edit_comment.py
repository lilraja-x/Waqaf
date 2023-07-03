"""
This module defines the route for editing a comment.

It includes a route for editing a comment in the Xonnet system.

Routes:
    - /comment/edit (PUT, PATCH): Edit a comment.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Comment, Post, User, db

edit_comment_bp = Blueprint('edit_comment', __name__)

@edit_comment_bp.route('/comment/edit', methods=['PUT', 'PATCH'])
@jwt_required(refresh=True)
def edit_comment():
    """Edit a comment.

    This route is used to edit a comment in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - user_id: The ID of the user who owns the comment.
        - post_id: The ID of the post the comment belongs to.
        - content: The updated content of the comment.

    Returns:
        jsonify: A JSON response indicating the success or failure of the comment editing operation.
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

    existing_comment = Comment.query.filter_by(user_id=user_id, post_id=data['post_id'], post_commented_of_id=data['user_id']).first()
    if not existing_comment:
        return jsonify({"Message": "Comment not found"}), 404

    if 'content' in data:
        existing_comment.content = data['content']

    try:
        db.session.commit()
        return jsonify({"Message": "Comment updated successfully"}), 200
    except Exception as e:
        return jsonify({"Message": "Failed to update comment!", "Error": str(e)}), 400
