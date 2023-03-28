virtualenv env
source env/Scripts/activate
pip3 install -r requirements.txt
export FLASK_APP=run.py
export FLASK_ENV=development
flask run