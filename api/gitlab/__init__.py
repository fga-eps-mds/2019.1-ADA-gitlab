# api/gitlab/__init__.py

import os
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine


# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


# instantiate the db
db = MongoEngine()
db.init_app(app)


@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
