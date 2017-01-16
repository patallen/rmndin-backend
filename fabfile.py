from fabric.api import env, run, cd
from fabric.network import ssh

ssh.util.log_to_file("paramiko.log", 10)

env.hosts = ['10.10.10.2']
env.user = 'vagrant'
env.password = 'vagrant'


def runserver():
    run("/var/rmndinenv/bin/python /var/rmndin/manage.py runserver")


def celery_worker():
    with cd('/var/rmndin'):
        run("/var/rmndinenv/bin/celery -A tasks worker --loglevel=info")
