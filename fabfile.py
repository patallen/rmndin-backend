from fabric.api import env, run
from fabric.network import ssh

ssh.util.log_to_file("paramiko.log", 10)

env.user = 'vagrant'
env.password = 'vagrant'
env.hosts = ['10.10.10.2']

def runserver():
    run("/var/rmndinenv/bin/python /var/rmndin/manage.py runserver")
