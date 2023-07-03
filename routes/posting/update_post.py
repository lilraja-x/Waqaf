"""
This module defines the routes related to updating a post.

It includes a route for editing a post in the Xonnet system.

Routes:
    - /post/edit (PUT, PATCH): Edit a post.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Post, db


update_post_bp = Blueprint('update_post', __name__)

@update_post_bp.route('/post/edit', methods=['PUT', 'PATCH'])
@jwt_required(refresh=True)
def edit_post():
    """Edit a post.

    This route is used to edit a post in the Xonnet system.
    It requires authentication with a valid access token.

    Request Body:
        - post_id: The ID of the post to be edited.
        - content (optional): The updated content of the post.
        - image (optional): The updated image URL of the post.

    Returns:
        jsonify: A JSON response indicating the success or failure of the post edit.
    """
    userid = get_jwt_identity()
    if not userid:
        return jsonify({"Message": "Token Invalid"}), 500

    # get data -->
    data = request.json

    # if the login credentials are correct
    if userid:
        try:
            # Fetch the post IDs associated with the user from the database
            user = User.query.get(userid)
            user_post_ids = [post.id for post in user.posts]

            # Get the post ID to be edited from the request data
            user_provided_post_id = data.get('post_id')

            if user_provided_post_id is not None:
                # Map the user's post IDs to a sequential numbering starting from 1
                mapped_post_ids = {i + 1: post_id for i, post_id in enumerate(user_post_ids)}

                # Find the actual post ID in the database based on the user's provided post ID
                if user_provided_post_id in mapped_post_ids:
                    actual_post_id = mapped_post_ids[user_provided_post_id]

                    # Update the data dictionary with the actual post ID and user ID
                    data['post_id'] = actual_post_id
                    data['user_id'] = userid

                    # Get the existing post
                    existing_post = Post.query.get(actual_post_id)

                    # Update the post content and image if provided
                    if 'content' in data:
                        existing_post.content = data['content']
                    if 'image' in data:
                        existing_post.image_url = data['image']

                    db.session.commit()

                    return jsonify({"Message": "Post Updated!"}), 200
                else:
                    return jsonify({"Message": "Post not found"}), 404
            else:
                return jsonify({"Message": "No post ID provided"}), 400
        except Exception as e:
            return jsonify({"Message": "Unable to edit post", "Error": str(e)}), 400
    else:
        return jsonify({"Message": "Account Not Found"}), 400