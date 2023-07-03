"""
This module defines the routes related to user login and authentication.

It includes a route for user login.

Routes:
    - /login (POST): Perform user login and authentication.
"""
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import jsonify, request, Blueprint, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User, db
from flask_mail import Mail, Message
from components.logging import Login
from routes.account.reset_tokens.RESETTOKENS import RESETTOKENS

user_login_bp = Blueprint('login', __name__)

login = Login()

@user_login_bp.route('/login', methods=['POST'])
def user_login():
    """Perform user login and authentication.
    
    This route is used to perform user login and authentication in the Xonnet system.
    It expects the following required fields in the request form data:
        - username
        - password
    
    Optional fields for password reset:
        - forgotten_password
    
    Returns:
        jsonify: A JSON response indicating the success or failure of the login operation.
            If successful, it includes the access token and refresh token for the user.
    """
    
    data = request.form
    mail = Mail(current_app)
    if 'username' not in data:
        return jsonify({"Message": "Username missing!"}), 401
    if 'password' not in data:
        return jsonify({"Message": "Password missing!"}), 401
    
    if data['password'] == '' and data.get('forgotten_password', '').lower() == 'true':
        user = User.query.filter_by(username=data['username']).first()
        if user:
            reset_token = user.get_reset_token(expires=3600)
            RESETTOKENS.add(reset_token)
            msg = Message("Password Reset", recipients=[user.email])
            msg.body = f"To reset your password, copy the reset token below :\n\n{reset_token}"
            mail.send(msg)
            
            return jsonify({"Message": "Password reset token has been sent to your email."}), 200
        else:
            return jsonify({"Message": "User not found!"}), 404
    
    elif data.get('forgotten_password', '').lower() == 'false':
        try:
            user = login.check(data)
            return jsonify({'Message': 'Logged In!', 'access token': user[0], 'refresh token': user[3]}), 200
        except Exception as e:
            return jsonify({"Message": "Failed to login!", "Error": str(e)}), 400

    else:
        return jsonify({"Message": "Value Error!"}), 401