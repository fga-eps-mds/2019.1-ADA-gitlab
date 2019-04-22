import os
from flask import Flask
from gitlab.pipeline.views import pipeline_blueprint
from gitlab.build.views import build_blueprint
from gitlab.report.views import report_blueprint
from flask_cors import CORS
from flask_mongoengine import MongoEngine


cors = CORS()
db = MongoEngine()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)
    cors.init_app(app)

    # register blueprints
    app.register_blueprint(pipeline_blueprint)
    app.register_blueprint(build_blueprint)
    app.register_blueprint(report_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
