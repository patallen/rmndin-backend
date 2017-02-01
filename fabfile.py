from fabric.api import env, run, cd
from fabric.network import ssh

ssh.util.log_to_file("paramiko.log", 10)
env.use_ssh_config = True

env.hosts = ['10.10.10.2']
env.user = 'vagrant'
env.password = 'vagrant'


def add_pip_requirement(name, version=None):
    version = "==%s" % version if version else ""
    with cd('/var/rmndin'):
        run("/var/rmndinenv/bin/pip install %s%s" % (name, version))
        run("/var/rmndinenv/bin/pip freeze > requirements.txt")

def runserver():
    run("/var/rmndinenv/bin/python /var/rmndin/manage.py runserver")


def db_migrate(message):
    message = "-m '%s'" % message

    with cd('/var/rmndin'):
        run("/var/rmndinenv/bin/python /var/rmndin/manage.py db migrate %s"
            % message)


def db_upgrade():
    with cd('/var/rmndin'):
        run("/var/rmndinenv/bin/python /var/rmndin/manage.py db upgrade")


def celery_worker(loglevel="info"):
    with cd('/var/rmndin'):
        run(
            "/var/rmndinenv/bin/celery "
            "-A rmndin.tasks worker --loglevel={}".format(loglevel)
        )
