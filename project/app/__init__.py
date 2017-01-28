from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)

from views.reminders import reminders as remindersbp

app.register_blueprint(remindersbp, url_prefix='/reminders')