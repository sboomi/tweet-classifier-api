"""Init app here"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

# Instanciate Flask modules here
db = SQLAlchemy(engine_options={'connect_args': {'connect_timeout': 5}})
migrate = Migrate()

# Define create app here


def create_app(config_class=Config):
    # Initialize apps
    app = Flask(__name__)

    app.logger.debug(f"SQL Alchemy URI: {config_class.SQLALCHEMY_DATABASE_URI}")
    app.config.from_object(config_class)

    # Initialize modules
    db.init_app(app)
    CORS(app, resources=r'/api/v1/*')
    migrate.init_app(app, db)

    # Create DB if it doesn't exist
    with app.app_context():
        db.create_all()
    app.logger.debug("Initiated database")

    from src.api_spec import spec
    # Import routes
    from src.endpoints.models import models
    from src.endpoints.swagger import SWAGGER_URL, swagger_ui_blueprint
    from src.endpoints.tweets import tweets

    # register blueprints. ensure that all paths are versioned!
    app.register_blueprint(tweets, url_prefix="/api/v1/tweets")
    app.register_blueprint(models, url_prefix="/api/v1/models")

    app.logger.debug("Registered all routes")

    # register all swagger documented functions here
    with app.test_request_context():
        for fn_name in app.view_functions:
            if fn_name == 'static':
                continue
            app.logger.debug(f"Loading swagger docs for function: {fn_name}")
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

    # Instanciate JSON doc for Swagger UI
    @app.route("/api/swagger.json")
    def create_swagger_spec():
        """
        Swagger API definition.
        """
        return jsonify(spec.to_dict())

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    return app
