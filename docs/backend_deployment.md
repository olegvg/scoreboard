# Deployment of backend onto single server

Assume that running user is _username_.

Under the `username` user:

## 1. Create directory tree

        sudo mkdir /opt/production
        sudo setfacl -m u:username:rwx /opt/production
        mkdir /opt/production/{apps,log,virtual_envs}
        mkdir /opt/production/log/scoreboard
        mkdir /opt/production/virtual_envs/scoreboard

## 2. Prepare login environment for git+ssh access to repository as mentioned [here](ssh_to_git.md)

## 3. Clone the last version

        git clone git@github.com:username/scoreboard.git /opt/production/apps/scoreboard

## 4. Install `virtualenv` in Debian way

        apt-get install python-virtualenv

## 5. Create virtual environment

        virtualenv /opt/production/virtual_envs/scoreboard
        ln -s /opt/production/apps/scoreboard/requirements.txt /opt/production/virtual_envs/scoreboard/requirements.txt

## 6. Install devel `.deb`-s which are needed to build `psycopg2`

        apt-get install build-essential python-dev libpq-dev

## 7. Install backend's requirements into virtual environment 

        source /opt/production/virtual_envs/scoreboard/bin/activate
        pip install -r /opt/production/virtual_envs/scoreboard/requirements.txt

## 8. Prepare frontend application

Instructions [here](frontend_deployment.md)
 
## 9. Create symbolic link to `supervisord` config

        sudo ln -s /opt/production/apps/scoreboard/production/bl_scoreboard_supervisord.conf /etc/supervisor/conf.d/scoreboard_supervisord.conf

## 10. Create symbolic links to Nginx configs

        sudo ln -s /opt/production/apps/scoreboard/production/bl_scoreboard_nginx.conf /etc/nginx/sites-enabled/scoreboard

## 11. Restart the services

        service syslog-ng restart
        supervisorctl
            >stop all
            >reread
            >start all
        service nginx restart
