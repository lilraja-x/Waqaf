"""
This module defines the routes related to user signup and account creation.

It includes a route for creating a new user Xonnet account.

Routes:
    - /signup (POST): Create a new user Xonnet account.
"""
from flask import jsonify, request, Blueprint, config, current_app
from components.creating import Create

user_signup_bp = Blueprint('create', __name__)
create = Create()

@user_signup_bp.route('/signup', methods=['POST'])
def user_signup():
    """Create a new user Xonnet account.

    This route is used to create a new user account in the Xonnet system.
    It expects the following required fields in the request form data:
        - username
        - email
        - password
        - name
        - bio(optional)
        - profile_image_url(optional)

    Returns:
        jsonify: A JSON response indicating the success or failure of the account creation.
    """
    data = dict(request.form)
    required_keys = ['username', 'email', 'password', 'name']

    if all(key in data for key in required_keys):
        if not 'profil_image_url' in data:
            data['profile_image_url'] = ''
        if not 'bio' in data:
            data['bio'] = ''
        try:
            bcrypt = current_app.config['bcrypt']
            create.create_account(data, bcrypt)
            return jsonify({"Message": "Account Created"}), 200
        except Exception as e:
            return jsonify({"Message": "Failed to Create Account", "Error": str(e)}), 400
    else:
        return jsonify({"Message": "Missing Keys"}), 401