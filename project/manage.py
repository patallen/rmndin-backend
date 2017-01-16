from flask_script import Manager, Server
from flask import Flask
# from api import app

app = Flask(__name__)
manager = Manager(app)
manager.add_command("runserver", Server())

if __name__ == '__main__':
    manager.run()
