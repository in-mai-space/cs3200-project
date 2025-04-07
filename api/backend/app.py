from flask import Flask, jsonify

from backend.database import db
from backend.config import load_config
from backend.users.users_routes import users
from backend.organizations.organizations_routes import organizations
from backend.programs.programs_routes import programs
from backend.feedbacks.feedback_routes import feedbacks
from backend.applications.applications_routes import applications

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
    
    # Register routes for API endpoints
    app.logger.info('current_app(): registering blueprints with Flask app object.') 
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(organizations, url_prefix='/organizations')
    app.register_blueprint(programs, url_prefix='/programs')
    app.register_blueprint(applications, url_prefix='/applications')
    app.register_blueprint(feedbacks, url_prefix='/feedbacks')

    return app
