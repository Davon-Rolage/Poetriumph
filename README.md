# Poetriumph Django Project
Poetriumph is a python/django project to translate poems from one language to another and save them to the PostgreSQL database.
## Installation
1. Create a virtual environment with `python -m venv venv`
1. Activate it with `venv\scripts\activate`
1. Install required dependencies with `python -m pip install -r requirements.txt`
1. Create a `.env` file in the root directory of your project. Add the following variables:
```
SECRET_KEY="your_django_secret_key"
OPENAI_API_KEY="your_openai_api_key"
POSTGRES_DB="name_of_postgresql_database"
POSTGRES_USER="your_postgresql_username"
POSTGRES_PASSWORD="your_postgresql_password"
PG_CONTAINER_NAME="your_postgres_container_name"
WEB_CONTAINER_NAME="your_web_container_name"
PGDATA=/data/davon-postgres

EMAIL_FROM="example@gmail.com"
EMAIL_HOST_USER="example@gmail.com"
EMAIL_HOST_PASSWORD="some_password"

RECAPTCHA_PUBLIC_KEY="your_recaptcha_public_key"
RECAPTCHA_PRIVATE_KEY="your_recaptcha_private_key"

ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1

DEBUG=1
```
___
### Email Confirmation upon registration
5. Go to [https://myaccount.google.com](https://myaccount.google.com) -> Security -> 2-Step Verification (it has to be ON) -> App passwords.
1. Create a new app name and put the shown password to `EMAIL_HOST_PASSWORD` variable in `.env`
___
### reCAPTCHA implementation
7. Go to [https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)
1. Press `Switch to create a classic key`
1. Create a label, select `reCAPTCHA v2` and `"I'm not a robot" Checkbox`
1. Add a domain, e.g. `mysite.com` or `127.0.0.1` (localhost).
1. Accept their Terms of Service and press Submit.
1. Copy `Site Key` to `RECAPTCHA_PUBLIC_KEY` variable in `.env`
1. Copy `Secret Key` to `RECAPTCHA_PRIVATE_KEY` variable in `.env`
___
14. Create a superuser with `python manage.py createsuperuser`
1. Make migrations and migrate:
```
python manage.py makemigrations
python manage.py migrate
```
16. Set `DEBUG` to `False` before deploying to production.
1. Run server with `python manage.py runserver`
___
## Add a new language interface
1. Add a folder for a new language with `django-admin makemessages -l <language-code>`
<br>For example, if you want to add French, enter `django-admin makemessages -l fr`
* [Full list of languages and language codes (Wikipedia)](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
2. Go to the file with translations: `locale/<language-code>/LC_MESSAGES/django.po`
1. Fill the empty space of every `msgstr` with the translation. For example:
```
#: .\poetry_translation\config.py:4
msgid "Detect language"
msgstr "Détecter la langue"
```
4. Compile all translations with `python manage.py compilemessages`
1. Update `base.html` to add the new language to the dropdown menu. Change `language_code` with your language:
```html
...
{% elif request.LANGUAGE_CODE == '<language_code>' %}
<img class="image-flag me-1" src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>">Some Language
...
<a class="dropdown-item" href="/<lang_code>/{{ request.path|remove_language }}"><img class="image-flag me-1" src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>">Some Language</a>
```