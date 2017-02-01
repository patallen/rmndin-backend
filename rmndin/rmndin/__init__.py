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


from views.reminders import reminders as remindersbp
from views.users import users as usersbp

app.register_blueprint(remindersbp, url_prefix='/reminders')
app.register_blueprint(usersbp, url_prefix='/users')
