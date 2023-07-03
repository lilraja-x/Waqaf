from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import User, Messaging, db

messaging_bp = Blueprint("Messaging", __name__)

@messaging_bp.route('/message/send', methods=['POST'])
@jwt_required(refresh=True)
def send_message():
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.get(user_id)

    if not user:
        return jsonify({"Message": "User not found"}), 404

    receiver_id = request.form.get('receiver_id')
    message = request.form.get('message')
    image = request.files.get('image')
    video = request.files.get('video')
    document = request.files.get('document')

    if not receiver_id:
        return jsonify({"Message": "To whom are you sending this message?"}), 401

    if not (message or image or video or document):
        return jsonify({"Message": "At least add some text, image, video, or document to send a message"}), 401

    try:
        new_message = Messaging(
            sender_id=user_id,
            receiver_id=receiver_id,
            message=message
        )

        if image:
            new_message.image_data = image.read()
            new_message.image_name = 'IMG01'
        if video:
            new_message.video_data = video.read()
            new_message.video_name = 'VID01'
        if document:
            new_message.document_data = document.read()
            new_message.document_name = 'DOC01'

        db.session.add(new_message)
        db.session.commit()

        return jsonify({"Message": "Message Sent!"}), 200
    except Exception as e:
        return jsonify({"Message": "Message Not Sent!", "Error": str(e)}), 400

@messaging_bp.route('/message/edit', methods=['PUT', 'PATCH'])
@jwt_required(refresh=True)
def edit_message():
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.get(user_id)

    if not user:
        return jsonify({"Message": "User not found"}), 404

    data = request.json
    message_id = data.get('message_id')
    new_message = data.get('message')

    if not message_id:
        return jsonify({"Message": "Invalid message ID"}), 401

    message = Messaging.query.get(message_id)

    if not message:
        return jsonify({"Message": "Message does not exist"}), 404

    try:
        message.message = new_message
        db.session.commit()
        return jsonify({"Message": "Message Edited!"}), 200
    except Exception as e:
        return jsonify({"Message": "Message Not Edited!", "Error": str(e)}), 400

@messaging_bp.route('/message/delete', methods=['DELETE'])
@jwt_required(refresh=True)
def delete_message():
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"Message": "Token Invalid"}), 500

    user = User.query.get(user_id)

    if not user:
        return jsonify({"Message": "User not found"}), 404

    data = request.json
    message_id = data.get('message_id')

    if not message_id:
        return jsonify({"Message": "Invalid message ID"}), 401

    message = Messaging.query.get(message_id)

    if not message:
        return jsonify({"Message": "Message does not exist"}), 404

    if message.sender_id != user_id:
        return jsonify({"Message": "You are not authorized to delete this message"}), 401

    try:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"Message": "Message Deleted!"}), 200
    except Exception as e:
        return jsonify({"Message": "Message Not Deleted!", "Error": str(e)}), 400
