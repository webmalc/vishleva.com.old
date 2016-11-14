from fabric.api import *

env.hosts = ['52.57.111.193']
env.port = 22
env.key_filename = '/home/webmalc/Documents/vishleva.pem'
env.user = "ubuntu"
env.project_dir = '/home/ubuntu/python/vishleva.com'
env.activate = 'source /home/ubuntu/.virtualenvs/vishleva/bin/activate'


def deploy():
    with cd(env.project_dir):
        with prefix(env.activate):
            run('git pull origin master')
            run('pip install -r requirements.txt')
            run('./manage.py collectstatic --no-input')
            run('./manage.py migrate --no-input')
    sudo('sudo supervisorctl restart vishleva')
    sudo('sudo service nginx restart')
