import os
import os
import re

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import sed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

f = open('secrets/inventory')
text = f.read()

env.hosts= list(re.search(".*ansible_ssh_host=(.+?)\s", text).groups())
env.user = 'deploy-kodkollektivet'
env.key_filename = './secrets/kodkollektivetse-deploy-user'


def _restart_services():
    run('sudo /bin/systemctl enable kodkollektivetse-celery.service')
    run('sudo /bin/systemctl enable kodkollektivetse.service')
    run('sudo /bin/systemctl restart kodkollektivetse-celery.service')
    run('sudo /bin/systemctl restart kodkollektivetse.service')
    run('sudo /bin/systemctl restart nginx.service')


def bootstrap(branch='ansible'):
    run('mkdir -p /srv/kodkollektivetse/current')
    run('mkdir -p /srv/kodkollektivetse/backups')
    run('mkdir -p /srv/kodkollektivetse/repo')
    run('mkdir -p /srv/kodkollektivetse/tmp')
    run('mkdir -p /srv/kodkollektivetse/public/static')
    run('mkdir -p /srv/kodkollektivetse/public/media')

    put('secrets', '/srv/kodkollektivetse/')

    with cd('/srv/kodkollektivetse/repo'):
        run('git config --global user.email "John.Smith@example.com"')
        run('git config --global user.name "John Smith"')
        run('git clone https://github.com/Kodkollektivet/kodkollektivet.se.git .')
        run('git fetch --all')
        run('git checkout {}'.format(branch))
        run('git pull')


    with cd('/srv/kodkollektivetse'):
        run('cp -rf repo/* current')
        run('cp -f secrets/production.py current/settings/production.py')
        run('cp -f secrets/production.json current/settings/production.json')

    with cd('/srv/kodkollektivetse/current'):
        run('rm -rf ansible')
        run('rm -rf tests')
        run('rm -f docker-compose.yml')
        run('rm -f Dockerfile')
        run('rm -f README.org')
        run('virtualenv --python=/usr/bin/python3 venv')
        run('venv/bin/pip install -r requirements.txt')
        run('sed -i "s/settings.settings/settings.production/g" manage.py')
        run('sed -i "s/settings.settings/settings.production/g" settings/wsgi.py')
        run('venv/bin/python manage.py makemigrations')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py compilemessages -l sv -l en')
        run('venv/bin/python manage.py collectstatic --noinput')

    _restart_services()


def deploy(branch='celery-docker'):
    with cd('/srv/unitime'):
        run("tar -zcvf backups/\"unitime-$(date '+%Y-%m-%d-%H-%M')-$(cd repo && git branch | grep \* | cut -d ' ' -f2).tar.gz\" current")

    put('secrets', '/srv/unitime/')

    with cd('/srv/unitime/repo'):
        run('git fetch --all')
        run('git checkout {}'.format(branch))
        run('git reset --hard origin/{}'.format(branch))
        run('git pull')

    with cd('/srv/unitime'):
        run('cp -rf repo/* current')
        run('cp -f secrets/production.py current/settings/production.py')
        run('cp -f secrets/production.json current/settings/production.json')

    with cd('/srv/unitime/current'):
        run('rm -rf venv')
        run('virtualenv --python=/usr/bin/python3 venv')
        run('venv/bin/pip install -r requirements.txt')
        run('find . -type f -exec sed -i "s/settings.settings/settings.production/g" {} \;')
        run('venv/bin/python manage.py makemigrations')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py collectstatic --noinput')

    _restart_services()


def rollback():
    with cd('/srv/unitime/backups/'):
        run('cp $(ls -Art | tail -n 1) ../')
        run('rm -f $(ls -Art | tail -n 1)')

    with cd('/srv/unitime/'):
        run("mv -f current/ tmp/unitime-$(date '+%Y-%m-%d-%k-%M')-moved")
        run('tar -zxvf *.tar.gz')
        run('rm -f *.tar.gz')

    run('sudo /bin/systemctl restart unitime-celery.service')
    run('sudo /bin/systemctl restart unitime.service')
