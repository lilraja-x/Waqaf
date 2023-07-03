"""
This module defines the routes related to deleting a post.

It includes a route for deleting a post from the Xonnet system.

Routes:
    - /post/delete (DELETE): Delete a post.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from components.posting import Posting
from models import User

delete_post_bp = Blueprint('delete_post', __name__)

post = Posting()
@delete_post_bp.route('/post/delete', methods=['DELETE'])
@jwt_required(refresh=True)
def delete_post():
    """Delete a post.

    This route is used to delete a post from the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - post_id: The ID of the post to be deleted.

    Returns:
        jsonify: A JSON response indicating the success or failure of the post deletion.
    """
    userid = get_jwt_identity()
    if not userid:
        return jsonify({"Message": "Token Invalid"}), 500

    # if the login credentials are correct
    if userid:
        try:
            # Fetch the post IDs associated with the user from the database
            user = User.query.get(userid)
            user_post_ids = [post.id for post in user.posts]

            # Get the post ID to be deleted from the request data
            data = request.json
            user_provided_post_id = data.get('post_id')

            if user_provided_post_id is not None:
                # Map the user's post IDs to a sequential numbering starting from 1
                mapped_post_ids = {i + 1: post_id for i, post_id in enumerate(user_post_ids)}

                # Find the actual post ID in the database based on the user's provided post ID
                if user_provided_post_id in mapped_post_ids:
                    actual_post_id = mapped_post_ids[user_provided_post_id]

                    # Update the data dictionary with the actual post ID
                    data['post_id'] = actual_post_id
                    data['user_id'] = userid

                    # Delete the post using the updated data
                    post.delete_post(data)

                    return jsonify({"Message": "Post Deleted!"}), 200
                else:
                    return jsonify({"Message": "Post not found"}), 404
            else:
                return jsonify({"Message": "No post ID provided"}), 400
        except Exception as e:
            return jsonify({"Message": "Unable to delete post", "Error": str(e)}), 400
    else:
        return jsonify({"Message": "Account Not Found"}), 400

