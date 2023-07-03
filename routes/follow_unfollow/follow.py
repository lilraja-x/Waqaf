"""
This module defines the routes related to user following functionality.

It includes a route for following a user.

Routes:
    - /follow (POST): Follow a user.
"""
from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from components.following import Following
from components.logging import Login

follow_bp = Blueprint('follow', __name__)

login = Login()
followed = Following()

@follow_bp.route('/follow', methods=['POST'])
@jwt_required(refresh=True)
def follow():
    """Follow a user.

    This route is used to follow a user in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - username: The username of the user to follow.

    Returns:
        jsonify: A JSON response indicating the success or failure of the follow operation.
    """
    data = request.json
    userid = get_jwt_identity()
    if not userid:
        return jsonify({"Message": "Token Invalid"}), 500
    if 'username' in data:
        try:
            user = followed.followed_to(data=data['username'])

            followedid = user
            followerid = userid
            followed.followed_by(followerid, followedid)
            return jsonify({"Message": f"Successfully Followed {data['username']}"}), 200
        except Exception as e:
            return jsonify({"Message": f"Failed to follow {data['username']}", "Error": str(e)}), 400
    else:
        return jsonify({"Message": "At least tell whom to follow."}), 401

