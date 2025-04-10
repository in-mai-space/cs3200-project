from flask import Flask, jsonify, Blueprint

from backend.database import db
from backend.config import load_config
from backend.users.controllers import users
from backend.organizations.organizations_routes import organizations
from backend.programs.programs_routes import programs
from backend.feedbacks.feedback_routes import feedbacks
from backend.categories.controllers import categories
from backend.applications.applications_routes import applications
from backend.user_profiles.controllers import user_profiles


def create_app():
    app = Flask(__name__)

    # Load configuration
    config = load_config()
    
    # Set configuration values
    app.config.update(config)

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    # Add healthcheck endpoint
    @app.route('/healthcheck')
    def health_check():
        return jsonify({"status": "healthy"}), 200
    
    # Create API v1 blueprint
    api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
    
    # Register routes under API v1
    app.logger.info('current_app(): registering blueprints with Flask app object.') 
    api_v1.register_blueprint(users, url_prefix='/users')
    api_v1.register_blueprint(user_profiles, url_prefix='/user_profiles')
    api_v1.register_blueprint(organizations, url_prefix='/organizations')
    api_v1.register_blueprint(programs, url_prefix='/programs')
    api_v1.register_blueprint(applications, url_prefix='/applications')
    api_v1.register_blueprint(feedbacks, url_prefix='/feedbacks')
    api_v1.register_blueprint(categories, url_prefix='/categories')

    # Register the API v1 blueprint with the app
    app.register_blueprint(api_v1)

    return app
