from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from api import app, db

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)
migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()
