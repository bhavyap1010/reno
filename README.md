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

# Troubleshooting

## JSONDecodeError at /api/v1/auth/google/callback/

- This error usually means the backend is expecting JSON but received invalid or empty data.
- Make sure your frontend sends the correct `Content-Type: application/json` header and a valid JSON body.
- Check your Google OAuth client credentials and redirect URIs.
- Inspect the backend logs for the exact error details.
- If using Django REST Framework, ensure your view expects JSON and handles errors gracefully.
- **Tip:** If you are using a POST request, ensure you are sending data as JSON, not as form data. For example, use `fetch(..., { body: JSON.stringify(data), headers: { 'Content-Type': 'application/json' } })` in JavaScript.
- If the error persists, print the request body in your Django view to debug what is being received.
