# Pasteque

## About

**Pasteque** is a free and open source (MIT License) **Pastebin like**
application written in Python/Django.

An instance can be found at: [wyz.fr](https://wyz.fr).  The wyz.fr
instance is installed by ansible, the role is available here:
https://github.com/JulienPalard/playbooks/tree/master/roles/pasteque.


## Features

- Support any database supported by Django (Sqlite3, MySQL, PostgreSQL, Oracle, ...)
- Available in english, french .. and easily translatable into another languages.
- Syntax highlighting for a bunch of languages using Pygments.
- Public/private pastes (don't appear in the pastes history).
- Time-based or "page loads"-based pastes expiration.
- Password protection.
- Possibility to enable/disable renderers and to choose the default one.
- Limit pastes size.
- Pastes history.


## Running Pasteque

In a [venv](https://docs.python.org/3/library/venv.html), install the requirements:

    pip install -r requirements.txt

In `settings.py` edit:

    DISPLAY_NAME = 'YourCompany-Paste'
    COMPRESS_ENABLED = True
    SECRET_KEY = 'fill_a_secret_key_here'
    ALLOWED_HOSTS = ['localhost','127.0.0.1','paste.henriet.eu']

Create some needed directories:

    mkdir -p var/{logs,db}

Then create the database:

    ./manage.py migrate

Insert initial data (like known languages):

    ./manage.py loaddata initial

If you're in production collect static files:

    ./manage.py collectstatic

Run it:

    ./manage.py runserver
