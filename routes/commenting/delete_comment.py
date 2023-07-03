"""
This module defines the route for deleting a comment.

It includes a route for deleting a comment in the Xonnet system.

Routes:
    - /comment/delete (DELETE): Delete a comment.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Comment, Post, User, db

delete_comment_bp = Blueprint('delete_comment', __name__)


@delete_comment_bp.route('/comment/delete', methods=['DELETE'])
@jwt_required(refresh=True)
def delete_comment():
    """Delete a comment.

    This route is used to delete a comment in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - user_id: The ID of the user who owns the comment.
        - post_id: The ID of the post the comment belongs to.
        - content: The content of the comment to be deleted.

    Returns:
        jsonify: A JSON response indicating the success or failure of the comment deletion operation.
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

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"Message": "User not found"}), 404
    
    if data['post_id'] not in post_id_mapping.values():
        # Post ID doesn't exist for the user
        return jsonify({"Message": "Post not found"}), 404
    
    comment = Comment.query.filter_by(user_id=user_id, post_id=data['post_id'], post_commented_of_id=data['user_id'], content=data['content']).first()
    
    if not comment:
        return jsonify({"Message": "Comment not found"}), 404
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"Message": "Comment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"Message": "Failed to delete comment!", "Error": str(e)}), 400