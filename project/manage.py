from flask_script import Manager, Server
from flask import Flask
# from api import app

app = Flask(__name__)
manager = Manager(app)
manager.add_command("runserver", Server())


@manager.command
def add():
    from tasks import add, cancel_task
    print "Adding!"
    result = add.apply_async(countdown=10, args=(10, 10))
    print result
    cancel_task(result.id)

if __name__ == '__main__':
    manager.run()
