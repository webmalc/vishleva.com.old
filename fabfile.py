from fabric.api import *

env.hosts = ['vishleva.com']
env.port = 22
env.key_filename = '/home/webmalc/.ssh/vishleva.pem'
env.user = "ubuntu"
env.project_dir = '/home/ubuntu/python/vishleva.com'
env.activate = 'source /home/ubuntu/.virtualenvs/vishleva/bin/activate'


def deploy():
    with cd(env.project_dir):
        with prefix(env.activate):
            run('git pull origin master')
            run('pip install --upgrade pip')
            run('pip install -r requirements.txt')
            run('npm install')
            run('./manage.py collectstatic --no-input')
            run('./manage.py migrate --no-input')
            run('./manage.py compilemessages')
    sudo('sudo supervisorctl restart vishleva')
    sudo('sudo supervisorctl restart celery')
    sudo('sudo supervisorctl restart celery_beat')
    sudo('sudo service nginx restart')
