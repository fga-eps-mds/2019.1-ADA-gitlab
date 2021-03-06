import os
from flask import Flask
from gitlab.pipeline.views import pipeline_blueprint
from gitlab.report.views import report_blueprint
from gitlab.build.views import build_blueprint
from gitlab.webhook.views import webhook_blueprint
from gitlab.user.views import user_blueprint
from gitlab.rerun_pipeline.views import rerun_pipeline_blueprint
from gitlab.stable_deploy.views import stable_deploy_blueprint
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
    app.register_blueprint(report_blueprint)
    app.register_blueprint(webhook_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(rerun_pipeline_blueprint)
    app.register_blueprint(stable_deploy_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
