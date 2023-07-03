"""
Main Application Setup
"""
from config import MAIL_EMAIL, MAIL_PASSWORD, JWT_SECRET_KEY, MAIL_DEFAULT_SENDER

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import db
from routes.account.create_account import user_signup_bp
from routes.account.login_account import user_login_bp
from routes.search.searching import searching_bp
from routes.account.delete_account import delete_account_bp
from routes.account.update_password import update_password_bp
from routes.profile.view_profile import view_profile_bp
from routes.profile.edit_profile import edit_profile_bp
from routes.posting.add_post import add_post_bp
from routes.posting.delete_post import delete_post_bp
from routes.posting.update_post import update_post_bp
from routes.follow_unfollow.follow import follow_bp
from routes.follow_unfollow.unfollow import unfollow_bp
from routes.liking.like import like_bp
from routes.liking.unlike import unlike_bp
from routes.commenting.add_comment import add_comment_bp
from routes.commenting.edit_comment import edit_comment_bp
from routes.commenting.delete_comment import delete_comment_bp
from routes.messaging.messaging import messaging_bp

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = MAIL_EMAIL
# app.config['MAIL_PASSWORD'] = "hypotheticalmailid786"
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/Waqaf_DB'
app.config['bcrypt'] = Bcrypt(app)

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


def create_app(config):
    """
    Creates the Flask app with the provided configuration.

    Args:
        config: Configuration object for the Flask app.

    Returns:
        The Flask app instance.

    """
    return app


# Register blueprints
app.register_blueprint(user_signup_bp)
app.register_blueprint(delete_account_bp)
app.register_blueprint(user_login_bp)
app.register_blueprint(searching_bp)
app.register_blueprint(update_password_bp)
app.register_blueprint(add_post_bp)
app.register_blueprint(update_post_bp)
app.register_blueprint(delete_post_bp)
app.register_blueprint(follow_bp)
app.register_blueprint(unfollow_bp)
app.register_blueprint(like_bp)
app.register_blueprint(unlike_bp)
app.register_blueprint(add_comment_bp)
app.register_blueprint(edit_comment_bp)
app.register_blueprint(delete_comment_bp)
app.register_blueprint(view_profile_bp)
app.register_blueprint(edit_profile_bp)
app.register_blueprint(messaging_bp)
