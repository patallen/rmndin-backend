from fabric.api import env, run, cd
from fabric.network import ssh

ssh.util.log_to_file("paramiko.log", 10)
env.use_ssh_config = True

env.hosts = ['10.10.10.2']
env.user = 'vagrant'
env.password = 'vagrant'

BASEPATH = '/var/rmndin'
VENVPATH = '%senv' % BASEPATH
BIN_PATH = '%s/bin' % VENVPATH

FLASK_APP = 'rmndin/__init__.py'
APP_PATH = '%s/%s' % (BASEPATH, FLASK_APP)
ENVIRONMENT = {
    "FLASK_DEBUG": 1,
    "FLASK_APP": "%s/%s" %(BASEPATH, FLASK_APP)
}


def envars():
    envars = ["%s=%s" % (k, v) for k, v in ENVIRONMENT.iteritems()]
    return " ".join(envars)


def command(command):
    with cd('/var/rmndin'):
        run('%s %s/flask %s' % (envars(), BIN_PATH, command))


def add_requirement(name, version=None):
    version = "==%s" % version if version else ""
    with cd('/var/rmndin'):
        run("%s/pip install %s%s" % (BIN_PATH, name, version))
        run("%s/pip freeze > requirements.txt" % BIN_PATH)


def runserver(host='0.0.0.0', port=5000, debug=True, autoreload=True):
    args = "-h {host} -p {port}".format(host=host, port=port)
    if debug:
        args = "{args} --debugger".format(args=args)

    if autoreload:
        args = "{args} --reload".format(args=args)
    command("run {args}".format(args=args))


def db_migrate(message):
    message = "-m '%s'" % message
    command('db migrate %s' % message)


def db_upgrade():
    command("db upgrade")


def db_downgrade(revision="-1"):
    command("db downgrade %s" % revision)


def celery_worker(loglevel="info"):
    with cd('/var/rmndin'):
        run(
            "{}/celery "
            "-A rmndin.tasks worker --loglevel={}".format(BIN_PATH, loglevel)
        )
