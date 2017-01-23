from fabric.api import env, run, cd
from fabric.network import ssh

ssh.util.log_to_file("paramiko.log", 10)
env.use_ssh_config = True

env.hosts = ['10.10.10.2']
env.user = 'vagrant'
env.password = 'vagrant'


def runserver():
    run("/var/rmndinenv/bin/python /var/rmndin/manage.py runserver")


def db_migrate():
    with cd('/var/rmndin'):
        run("/var/rmndinenv/bin/python /var/rmndin/manage.py db migrate")


def db_upgrade():
    with cd('/var/rmndin'):
        run("/var/rmndinenv/bin/python /var/rmndin/manage.py db upgrade")


def celery_worker(loglevel="info"):
    with cd('/var/rmndin'):
        run(
            "/var/rmndinenv/bin/celery "
            "-A app.reminders.tasks worker --loglevel={}".format(loglevel)
        )
