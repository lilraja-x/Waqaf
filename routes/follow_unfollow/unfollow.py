"""
This module defines the routes related to user unfollowing functionality.

It includes a route for unfollowing a user.

Routes:
    - /unfollow (POST): Unfollow a user.
"""
from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from components.unfollowing import Unfollowing
from components.logging import Login
from models import User

unfollow_bp = Blueprint('unfollow', __name__)

login = Login()
unfollowed = Unfollowing()


@unfollow_bp.route('/unfollow', methods=['POST'])
@jwt_required(refresh=True)
def unfollow():
    """Unfollow a user.

    This route is used to unfollow a user in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - username: The username of the user to unfollow.

    Returns:
        jsonify: A JSON response indicating the success or failure of the unfollow operation.
    """
    data = request.json
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    if 'username' in data:
        try:
            user = User.query.filter_by(username=data['username']).first()

            if not user:
                return jsonify({"Message": "User not found."}), 404

            unfollowed_id = user.id
            unfollowed.unfollowed_by(user_id, unfollowed_id)

            # Get updated followers and following counts
            unfollower = User.query.get(user_id)
            followers_count = unfollower.followers.count()
            following_count = unfollower.following.count()

            return jsonify({
                "Message": f"Successfully unfollowed {data['username']}",
                "Followers Count": followers_count,
                "Following Count": following_count
            }), 200

        except Exception as e:
            return jsonify({"Message": f"Failed to unfollow {data['username']}","Error": str(e)}), 400

    else:
        return jsonify({"Message": "Please provide a username to unfollow."}), 401

