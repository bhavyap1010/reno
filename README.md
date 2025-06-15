Create a new Python virtual environment

python3 -m venv env

source env/bin/activate

python -m pip install -r requirements.txt
pip install django-cors-headers
pip install djangorestframework-simplejwt

python manage.py runserver


access the mobile app folder
    npm start
    npm install --legacy-peer-deps