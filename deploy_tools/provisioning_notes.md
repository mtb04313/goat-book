Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.10
* virtualenv + pip
* Git

eg, on Ubuntu:

    sudo apt update
    sudo apt install nginx git python3 python3-venv

## Nginx config
* e.g. /etc/nginx/nginx.conf
* replace: user www-data; 
*    with: user ubuntu;


## Nginx Virtual Host config

* e.g. /etc/nginx/sites-available/goat-book-staging-server
* replace DOMAIN with, e.g., ec2-XX-XXX-XX-XXX.ap-southeast-1.compute.amazonaws.com

## Systemd service

* e.g. /etc/systemd/system/gunicorn-goat-book-staging-server.service


## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── DOMAIN1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── DOMAIN2
         ├── .env
         ├── db.sqlite3
         ├── etc
         