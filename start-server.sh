#!/usr/bin/env bash

python manage.py collectstatic --noinput;  # create static pages
python manage.py makemigrations;  # create initial db migrations
python manage.py migrate;  # make the db

python manage.py runserver 0.0.0.0:8000;  # run the test server