from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import User


searching_bp = Blueprint("search", __name__)
@searching_bp.route('/search', methods=['GET'])
@jwt_required(refresh=True)
def search():
    data = request.json
    search = data['username']

    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"Message": "User not found"}), 404
    
    try:
        searched_user = User.query.filter_by(username=search).first()
        return jsonify({"Message": "User Found", "User": searched_user.username}), 200
    except:
        return jsonify({"Message": "No user found with this username"}), 401
