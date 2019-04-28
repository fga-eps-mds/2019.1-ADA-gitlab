import os
from flask import Flask
from gitlab.pipeline.views import pipeline_blueprint
from gitlab.build.views import build_blueprint
from flask_cors import CORS

cors = CORS()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    cors.init_app(app)

    # register blueprints
    app.register_blueprint(pipeline_blueprint)
    app.register_blueprint(build_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
