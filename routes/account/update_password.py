from flask import Blueprint, request, jsonify, current_app
from models import User, db
from routes.account.reset_tokens.RESETTOKENS import RESETTOKENS

update_password_bp = Blueprint('update_password', __name__)

@update_password_bp.route('/update/password', methods=['POST'])
def update_password():
    reset_token = request.form.get('reset_token')
    username = request.form.get('username')
    new_password = request.form.get('new_password')

    # Verify the reset token and update the password
    def reset_token_validation(reset_token):
        if reset_token in RESETTOKENS:
            return True
        else:
            raise Exception("Invalid reset token")

    def password_update(username, new_password):
        bcrypt = current_app.config['bcrypt']
        user = User.query.filter_by(username=username).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return True
        else:
            raise Exception("User not found")

    try:
        reset_token_validation(reset_token)
        password_update(username, new_password)
        return jsonify({"Message": "Password updated successfully."}), 200
    except Exception as e:
        return jsonify({"Message": "Failed to update password.", "Error": str(e)}), 400
