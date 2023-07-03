"""
This module defines the routes related to editing a user's profile.

It includes a route for editing a user's profile information in the Xonnet system.

Routes:
    - /profile/edit (PUT, PATCH): Edit user profile information.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import User, db

edit_profile_bp = Blueprint('edit_profile', __name__)

@edit_profile_bp.route('/profile/edit', methods=['PUT', 'PATCH'])
@jwt_required(refresh=True)
def edit_profile():
    """Edit user profile information.

    This route is used to edit a user's profile information in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - username (optional): The updated username of the user.
        - name (optional): The updated name of the user.
        - email (optional): The updated email of the user.
        - profile_image_url (optional): The updated profile image URL of the user.
        - bio (optional): The updated bio of the user.

    Returns:
        jsonify: A JSON response indicating the success or failure of the profile update.
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"Message": "User not found"}), 404
    try:
        data = dict(request.form)
        existing_profile_info = User.query.get(user_id)
        if 'username' in data:
            existing_profile_info.username = data['username']
        if 'name' in data:
            existing_profile_info.name = data['name']
        if 'email' in data:
            existing_profile_info.email = data['email']
        if 'profile_image_url' in data:
            existing_profile_info.profile_image_url = data['profile_image_url']
        if 'bio' in data:
            existing_profile_info.bio = data['bio']

        db.session.commit()

        return jsonify({"Message": "Profile Updated Successfully!"}), 200
    except:
        return jsonify({"Message": "Failed to edit profile!", "Error": str(Exception)}), 400
