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


from rmndin.reminders.views import reminders as remindersbp
from rmndin.users.views import users as usersbp
from rmndin.users.views import verify as verifybp

app.register_blueprint(remindersbp, url_prefix='/reminders')
app.register_blueprint(usersbp, url_prefix='/users')
app.register_blueprint(verifybp, url_prefix='/verify')
