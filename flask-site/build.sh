#!/usr/bin/env bash
# exit on error
set -o errexit

virtualenv env
source env/Scripts/activate
# pip3 install -r requirements.txt
export FLASK_APP=run.py
export FLASK_ENV=development
# python -m pip install --upgrade pip

# pip install -r requirements.txt

flask db init
flask db migrate
flask db upgrade
flask gen_api
flask run