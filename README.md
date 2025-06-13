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

    1. Make sure you have Node installed
    2. Install modules `yarn install`
    3. Create `.env.local` file and provide Google Client ID
    4. Run `yarn dev`



- cd mobile-app
- yarn android
- yarn ios
- yarn web
✨  Done in 9.43s.



yarn expo start