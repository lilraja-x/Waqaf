"""
This module defines the routes related to adding a post.

It includes a route for adding a post to the Xonnet system.

Routes:
    - /post/add (POST): Add a post.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from components.logging import Login
from components.posting import Posting


add_post_bp = Blueprint('add_post', __name__)

login = Login()
post = Posting()

@add_post_bp.route('/post/add', methods=['POST'])
@jwt_required(refresh=True)
def add_post():
    """Add a post.

    This route is used to add a post in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - content (optional): The content of the post.
        - image (optional): The image associated with the post.

    Returns:
        jsonify: A JSON response indicating the success or failure of the post addition.
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500
    # get dataa -->
    data = request.json

    # if the login credetionals are correct -->
    if user_id:

        # set user id to the returned user_id
        data['user_id'] = user_id

        # if there is no content or image in post, it is ok set them to null and let user post.
        if not 'content' in data:
            data['content'] = ''
        elif not 'image' in data:
            data['image'] = ''

        # but if both are not present raise an issue -->
        elif not 'content' and 'image' in data:
            return jsonify({"Message": "Atleast add content or image!"}), 401


        # after all that send data to the add_pst function which posts the data and saves it to database -->
        try:
            post.add_post(data)

            # then return the response -->
            return jsonify({"Message": "Post Added!", "Content": data['content'], "Image": data['image']}), 200
        except Exception as e:
            return jsonify({"Message": "Unable to add post", "Error": str(e)}), 400
    else:
        return jsonify({"Message": "Account Not Found"}), 400

