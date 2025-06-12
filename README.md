Create a new Python virtual environment

python -m venv env

source env/bin/activate

python -m pip install -r requirements.txt
#pip install django-cors-headers
pip install djangorestframework-simplejwt

python manage.py runserver


 - Frontend application

    1. Make sure you have Node installed
    2. Install modules `yarn install`
    3. Create `.env.local` file and provide Google Client ID
    4. Run `yarn dev`

GOOGLE_OAUTH_CLIENT_ID='642552962636-7aiu16ona083q7tnogeibavn8j6hh9al.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET='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'
GOOGLE_OAUTH_CALLBACK_URL='http://127.0.0.1:8000/api/v1/auth/google/callback/'
