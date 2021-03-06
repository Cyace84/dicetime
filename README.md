Install
=======

```
# Dependencies

$ apt-get install python3 python3-pip python3-venv
$ apt-get install python3-venv
$ apt-get install postgresql
# Configure postgresql 1: create database, user, grant user privileges on database
# Configure postgresql 2 (maybe you know more secure way): add line to pg_hba.conf: "local   dicetime   dicebot    trust"

# Setup project environment

$ git clone ...
$ cd ...
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ touch dice.env  # see dice.env.sample

# setup nginx conf (see reference conf from this repo)
# copy /root/dicetime/db.sqlite3 from dev server to project folder (needed for db initial content setup)

# Run it twice for SECRET_KEY and MNEMONIC_ENCRYPTION_KEY in .env
$ ./manage.py generate_encryption_key
$ ./manage.py createsuperuser
$ ./manage.py migrate
$ ./manage.py collectstatic  # css/js for admin. will use /var/www/static so make sure nginx serves it

$ (it was needed only once) ./manage.py sqlite2pg  # copy initial data from db.sqlite to PG
# tool to set/replace payout config
$ ./manage.py setaddr seed phrase words ...
```


Run and stop
============

Make sure you're in a virtualenv (`source .venv/bin/activate`)

Notes:
  - you can adjust worker count as you wish in `run.sh`
  - `run.sh` is blocking, so you may want to run it with `nohup` or `screen` tool

```
# run.sh
$ gunicorn --reload --access-logfile gunicorn.log --workers 4 --bind 127.0.0.1:8000 --pid gunicorn.pid dice_time.wsgi:application

$ ./manage.py setaddr seed phrase words ...
$ ./manage.py startjobs  # blocking

# stop.sh
kill `grep -hs ^ gunicorn.pid` 2>/dev/null
```
