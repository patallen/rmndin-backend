from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
import yaml


def yaml_update_config(app, path):
    with open(path, 'r') as yfile:
        ycontents = yaml.load(yfile)
        app.config.update(ycontents)

app = Flask(__name__)
app.config.from_pyfile('/var/rmndin/config.py')
yaml_update_config(app, '/var/rmndin/private.yml')
db = SQLAlchemy(app)

from rmndin.auth import jwt
jwt = JWT(app, jwt.authenticate, jwt.identity)


from rmndin.reminders.views import bp as reminders
from rmndin.users.views import usersbp as users
from rmndin.users.views import verifybp as verify
from rmndin.auth.views import bp as auth

app.register_blueprint(reminders, url_prefix='/api/users/<user_id>/reminders')
app.register_blueprint(users, url_prefix='/api/users')
app.register_blueprint(verify, url_prefix='/verify')
app.register_blueprint(auth)
