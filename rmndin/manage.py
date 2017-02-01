from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from rmndin import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
