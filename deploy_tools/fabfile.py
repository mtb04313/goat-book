import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/mtb04313/goat-book.git'
SHORT_NAME = 'goat-book-production-server'

def deploy():
    #site_folder = f'/home/{env.user}/sites/{env.host}'  
    site_folder = f'/home/{env.user}/sites/' + SHORT_NAME
    run(f'mkdir -p {site_folder}')  
    with cd(site_folder):  
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _provision_nginx_and_unicorn()


def _get_latest_source():
    if exists('.git'):  
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} .')  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}')  
    
    
def _update_virtualenv():
    if not exists('.venv/bin/pip'):  
        run(f'python3 -m venv .venv')
    run('./.venv/bin/pip install -r requirements.txt')
    
    
def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')  
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')  
    if 'DJANGO_SECRET_KEY' not in current_contents:  
        new_secret = ''.join(random.SystemRandom().choices(  
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files():
    run('./.venv/bin/python3 manage.py collectstatic --noinput')
    
    
def _update_database():
    run('./.venv/bin/python3 manage.py migrate --noinput') 
    
    
def _provision_nginx_and_unicorn():
    ENV_HOST = f'{env.host}'

    nginx_sed_cmd = 'cat ./deploy_tools/nginx.ssl.template.conf ' + \
              '| sed "s/DOMAIN/{}/g" '.format(ENV_HOST) +  \
              '| sed "s/SHORT_NAME/{}/g" '.format(SHORT_NAME) + \
              '| sudo tee /etc/nginx/sites-available/{}'.format(SHORT_NAME)
            
    nginx_ln_cmd = 'sudo ln -sf /etc/nginx/sites-available/{} '.format(SHORT_NAME) + \
                '/etc/nginx/sites-enabled/{}'.format(SHORT_NAME)
        
    gunicorn_sed_cmd = 'cat ./deploy_tools/gunicorn-systemd.template.service ' + \
        '| sed "s/SHORT_NAME/{}/g"'.format(SHORT_NAME) + \
        '| sudo tee /etc/systemd/system/gunicorn-{}.service'.format(SHORT_NAME)
    
    gunicorn_enable_cmd = 'sudo systemctl enable gunicorn-{}'.format(SHORT_NAME)
    
    gunicorn_start_cmd = 'sudo systemctl start gunicorn-{}'.format(SHORT_NAME)
        
    run(nginx_sed_cmd)
    run(nginx_ln_cmd)
    run(gunicorn_sed_cmd)
    
    run('sudo systemctl daemon-reload')
    run('sudo systemctl reload nginx')
    
    run(gunicorn_enable_cmd)
    run(gunicorn_start_cmd)


def test():
    ENV_HOST = 'ec2-13-250-59-234.ap-southeast-1.compute.amazonaws.com'

    nginx_sed_cmd = 'cat ./deploy_tools/nginx.ssl.template.conf ' + \
              '| sed "s/DOMAIN/{}/g" '.format(ENV_HOST) +  \
              '| sed "s/SHORT_NAME/{}/g" '.format(SHORT_NAME) + \
              '| sudo tee /etc/nginx/sites-available/{}'.format(SHORT_NAME)
            
    nginx_ln_cmd = 'sudo ln -sf /etc/nginx/sites-available/{} '.format(SHORT_NAME) + \
                '/etc/nginx/sites-enabled/{}'.format(SHORT_NAME)
        
    gunicorn_sed_cmd = 'cat ./deploy_tools/gunicorn-systemd.template.service ' + \
        '| sed "s/SHORT_NAME/{}/g"'.format(SHORT_NAME) + \
        '| sudo tee /etc/systemd/system/gunicorn-{}.service'.format(SHORT_NAME)
    
    gunicorn_enable_cmd = 'sudo systemctl enable gunicorn-{}'.format(SHORT_NAME)
    
    gunicorn_start_cmd = 'sudo systemctl start gunicorn-{}'.format(SHORT_NAME)
        
    print(nginx_sed_cmd)
    print(nginx_ln_cmd)
    print(gunicorn_sed_cmd)
    
    print('sudo systemctl daemon-reload')
    print('sudo systemctl reload nginx')
    
    print(gunicorn_enable_cmd)
    print(gunicorn_start_cmd)
