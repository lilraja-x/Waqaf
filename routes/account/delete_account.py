"""
This module defines the route for deleting a user account.

It includes a route for deleting a user account from the Xonnet system.

Routes:
    - /delete (DELETE): Delete a user account.
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import User, db, Post, Follow, Comment, Like

delete_account_bp = Blueprint('delete_account', __name__)

@delete_account_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Delete a user account.

    This route is used to delete a user account from the Xonnet system.
    It requires authentication with a valid access token.

    Returns:
        jsonify: A JSON response indicating the success or failure of the account deletion operation.
    """
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.get(user_id)
    if not user:
        return jsonify({"Message": "User not found"}), 404

    try:
        Post.query.filter_by(user_id=user_id).delete()
        Follow.query.filter_by(follower_id=user_id).delete()
        Follow.query.filter_by(followed_id=user_id).delete()
        Comment.query.filter_by(user_id=user_id).delete()
        Like.query.filter_by(user_id=user_id).delete()

        db.session.delete(user)
        db.session.commit()

        return jsonify({"Message": "Account deleted successfully!"}), 200
    except:
        db.session.rollback()
        return jsonify({"Message": "Failed to delete account!"}), 400