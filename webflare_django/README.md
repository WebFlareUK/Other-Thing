Django integration of webflare_signoff

Setup (macOS):

1. Create a virtualenv and install:

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run migrations:

   python manage.py migrate

3. Create a superuser to view submissions in admin (optional):

   python manage.py createsuperuser

4. Run server:

   python manage.py runserver

5. Open http://127.0.0.1:8000/ to view and submit the sign-off form.

Notes:
- Place your real logo file at static/signoff/WebFlare-Logo.png
- For production, update SECRET_KEY, DEBUG, ALLOWED_HOSTS, and configure a proper media/static hosting solution.
- The signature is saved as an image to MEDIA_ROOT/signatures/ and referenced by the SignOff model.
