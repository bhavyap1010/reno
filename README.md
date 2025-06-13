Create a new Python virtual environment

python3 -m venv env

source env/bin/activate

python -m pip install -r requirements.txt
pip install django-cors-headers
pip install djangorestframework-simplejwt

python manage.py runserver


 - Frontend application
access the frontend folder

npm install -g yarn

- cd mobile-app
- yarn android
- yarn ios
- yarn web
✨  Done in 9.43s.

yarn expo start --web (this one is for web)