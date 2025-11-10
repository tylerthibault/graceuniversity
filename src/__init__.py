import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional
from flask import Flask

"""Flask application initialization and configuration.

This module creates and configures the Flask application instance,
initializes the database, registers blueprints, and sets up logging.
"""

# Import db from models module (single source of truth)
from src.models import db

def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure Flask application instance.
    
    Args:
        config_name: Configuration environment name (development, production, testing)
                    Defaults to value from FLASK_ENV environment variable
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    _configure_app(app, config_name)
    _load_db_tables(app)
    
    # Initialize extensions
    _init_extensions(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Setup logging
    _init_logging(app)
    
    return app


def _configure_app(app: Flask, config_name: Optional[str]) -> None:
    """Load application configuration.
    
    Args:
        app: Flask application instance
        config_name: Configuration environment name
    """
    # Get base directory (project root)
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    instance_dir = os.path.join(basedir, 'instance')
    
    # Create instance directory if it doesn't exist
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    # Database path in instance folder
    db_path = os.path.join(instance_dir, 'grace_university.db')
    
    # Default configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{db_path}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

def _load_db_tables(app: Flask) -> None:
    """Load database table definitions.
    
    Args:
        app: Flask application instance
    """
    # Import all models to register them with SQLAlchemy
    from src.models.user import User
    from src.models.role import Role


def _init_extensions(app: Flask) -> None:
    """Initialize Flask extensions.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()


def _register_blueprints(app: Flask) -> None:
    """Register application blueprints.
    
    Args:
        app: Flask application instance
    """
    from src.controllers.routes import main
    app.register_blueprint(main)

    from src.controllers.auth import auth_bp
    app.register_blueprint(auth_bp)

    from src.controllers.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Register error handlers
    _register_error_handlers(app)
    


def _register_error_handlers(app: Flask) -> None:
    """Register application error handlers.
    
    Args:
        app: Flask application instance
    """
    from flask import render_template
    from typing import Tuple
    
    @app.errorhandler(404)
    def not_found(error) -> Tuple[str, int]:
        """Handle 404 Not Found errors.
        
        Args:
            error: The error object passed by Flask
            
        Returns:
            Tuple of (rendered HTML template, 404 status code)
        """
        return render_template('public/error/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error) -> Tuple[str, int]:
        """Handle 500 Internal Server errors.
        
        Args:
            error: The error object passed by Flask
            
        Returns:
            Tuple of (rendered HTML template, 500 status code)
        """
        return render_template('public/error/500.html'), 500


def _init_logging(app: Flask) -> None:
    """Configure application logging.
    
    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Setup file handler with rotation
        file_handler = RotatingFileHandler(
            'logs/grace_university.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        # Set logging format
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Add handler to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Grace University application startup')
    else:
        # Console logging for development
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Grace University application startup (DEBUG mode)')