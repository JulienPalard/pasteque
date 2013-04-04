Pasteque
========

About
-----
**Pasteque** is a free and open source (MIT License) **Pastebin like** application written in Python/Django.

Demo
----
A **demo** instance of **Pasteque** is running at [http://paste.henriet.eu](http://paste.henriet.eu).

Features
--------
- Support any database supported by Django (Sqlite3, MySQL, PostgreSQL, Oracle, ...)
- Available in english, french .. and easily translatable into another languages.
- Syntax highlighting for a bunch of languages using Pygments.
- Public/private pastes (don't appear in the pastes history).
- Time-based or "page loads"-based pastes expiration.
- Password protection.
- Possibility to enable/disable renderers and to choose the default one.
- Limit pastes size.
- Pastes history.

Upcoming releases features
--------------------------
- Duplicate paste
- Locale selector
- Search engine
- Disable pastes via link submitted by email
- Copy to clipboard JS
- Google Analytics easy-integration

Deployment with Sqlite3, nginx and UWSGI
----------------------------------------

This procedure will guide you step-by-step through the setup of your own instance of **Pasteque** using
nginx et UWSGI. In this tutorial, app files and servers processes are owned by unprivilegied **web** user.

### Pre-required system packages

It is assumed that some system packages are installed on the server where you plan to setup **Pasteque**.

**On Debian**
<pre>
sudo apt-get install python python-pip python-dev nginx git
</pre>

### Application deployment

The application is deployed into **/opt/app/webtools** which is owner by user **web**.

<pre>
sudo mkdir -p /opt/app/webtools/
sudo chown -R web: /opt/app/webtools/
cd /opt/app/webtools/
git clone https://github.com/setsuna-/pasteque .
mkdir -p var/logs var/db var/pygments-static
</pre>

### Install required python packages

Even if python packages are installed system-wide in this tutorial, **virtualenv** is of course the way to go.

<pre>
sudo -s
export CFLAGS="-march=native -O2 -fomit-frame-pointer -pipe" && export CXXFLAGS="-march=native -O2 -fomit-frame-pointer -pipe"
pip install -r /opt/app/webtools/share/requirements.pip
</pre>

### Pasteque configuration and customization

<pre>
vim /opt/app/webtools/webtools/settings.py
DISPLAY_NAME = 'YourCompany-Paste'
COMPRESS_ENABLED = True
SECRET_KEY = 'fill_a_secret_key_here'
ALLOWED_HOSTS = ['localhost','127.0.0.1','paste.henriet.eu']
</pre>

### Sqlite3 database creation

<pre>
cd /opt/app/webtools/
./manage.py syncdb
Creating tables ...
Creating table paste_language
Creating table paste_paste
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)
sqlite3 var/db/webtools.sqlite3
sqlite> .read share/language-dml.sql
sqlite> .quit
</pre>

### Deploy static assets

<pre>
./manage.py collectstatic
ls static/
css  font  img  js
</pre>

### Test application

Validate application setup using the development web server.

<pre>
./manage.py runserver paste.henriet.eu:16000
</pre>

### Configure UWSGI

<pre>
cp /opt/app/webtools/share/uwsgi.ini /opt/app/webtools/uwsgi.ini
vim /opt/app/webtools/uwsgi.ini
[uwsgi]
chdir=/opt/app/webtools
module=webtools.wsgi:application
master=True
env=DJANGO_SETTINGS_MODULE=webtools.settings
pidfile=/opt/app/webtools/var/uwsgid-pasteque.pid
socket=/opt/app/webtools/var/uwsgid-pasteque.sock
processes=5
uid=1002
gid=1002
harakiri=20
limit-as=128
max-requests=5000
vacuum=True
daemonize=/opt/app/webtools/var/uwsgid-pasteque.log
</pre>

### Run UWSGI

<pre>
uwsgi --ini /opt/app/webtools/uwsgi.ini
[uWSGI] getting INI configuration from /opt/app/webtools/uwsgi.ini
ps -ef |grep uwsgi
web     2269     1  0 11:32 ?        00:00:00 uwsgi --ini /opt/app/webtools/uwsgi.ini
web     2271  2269  0 11:32 ?        00:00:00 uwsgi --ini /opt/app/webtools/uwsgi.ini
web     2272  2269  0 11:32 ?        00:00:00 uwsgi --ini /opt/app/webtools/uwsgi.ini
web     2273  2269  0 11:32 ?        00:00:00 uwsgi --ini /opt/app/webtools/uwsgi.ini
web     2274  2269  0 11:32 ?        00:00:00 uwsgi --ini /opt/app/webtools/uwsgi.ini
web     2275  2269  0 11:32 ?        00:00:00 uwsgi --ini /opt/app/webtools/uwsgi.ini
cat /opt/app/webtools/var/uwsgid-pasteque.log to check if everything is ok.
</pre>

### Configure NGINX

<pre>
sudo vim /etc/nginx/nginx.conf
user web;
sudo vim /etc/nginx/sites-available/webtools-pasteque
upstream uwsgi {
  server unix:///opt/app/webtools/var/uwsgid-pasteque.sock;
}
server {
  listen               80;
  server_name          paste.henriet.eu;
  charset              utf-8;
  error_log            /opt/app/webtools/var/nginx-error.log;
  access_log           /opt/app/webtools/var/nginx-access.log;
  client_max_body_size 8M;
  
  location /static {
    alias /opt/app/webtools/static;
    expires 30d;
  }

  location / {
    uwsgi_pass uwsgi;
    include    /etc/nginx/uwsgi_params;
  }
}
cd /etc/nginx/sites-enabled/
sudo ln -s ../sites-available/webtools-pasteque
</pre>

### Run nginx

<pre>
sudo /etc/init.d/nginx restart
Restarting nginx: nginx.
</pre>
