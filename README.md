# Poetriumph Django Project
Poetriumph is a Django project that allows users to translate poems from one language to another and save them to the PostgreSQL database.
## Installation
1. Create a virtual environment with `python -m venv venv`
1. Activate it with `venv\scripts\activate`
1. Install required dependencies with `python -m pip install -r requirements.txt`
1. Create a `.env` file which contains environment variables in the root directory of your project. Add the following variables:
```
SECRET_KEY="your_django_secret_key"
OPEN_API_KEY="your_openai_api_key"
POSTGRES_DB="name_of_postgresql_database"
POSTGRES_USER="your_postgresql_username"
POSTGRES_PASSWORD="your_postgresql_password"

EMAIL_FROM='example@gmail.com'
EMAIL_HOST_USER='example@gmail.com'
EMAIL_HOST_PASSWORD='some_password'

RECAPTCHA_PUBLIC_KEY='your_recaptcha_public_key'
RECAPTCHA_PRIVATE_KEY='your_recaptcha_private_key'
```
5. In the project's settings `poetriumph/settings.py`, change the `DATABASES` variable to match your name of the `HOST` and `PORT`
___
### Email Confirmation upon registration
6. Go to [https://myaccount.google.com](https://myaccount.google.com) -> Security -> 2-Step Verification (it has to be ON) -> App passwords.
7. Create a new app name and put the shown password to `EMAIL_HOST_PASSWORD` variable in `.env`
___
### reCAPTCHA implementation
8. Go to [https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)
9. Press `Switch to create a classic key`
1. Create a label, select `reCAPTCHA v2` and `"I'm not a robot" Checkbox`
1. Add a domain, e.g. `mysite.com` or `127.0.0.1` (localhost).
1. Accept their Terms of Service and press Submit.
1. Copy `Site Key` to `RECAPTCHA_PUBLIC_KEY` variable in `.env`
1. Copy `Secret Key` to `RECAPTCHA_SECRET_KEY` variable in `.env`
___
15. Create a superuser with `python manage.py createsuperuser`
1. Make migrations and migrate:
```
python manage.py makemigrations
python manage.py migrate
```
17. Set `DEBUG` to `False` before deploying to production.
18. Run server with `python manage.py runserver`
___
## Add a new language interface
1. Add a folder for a new language with `django-admin makemessages -l <language-code>`
<br>For example, if you want to add French, enter `django-admin makemessages -l fr`
* [Full list of languages and language codes (Wikipedia)](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
2. Go to the file with translations: `locale/<language-code>/LC_MESSAGES/django.po`.
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
Language
...
<a class="dropdown-item" href="/<lang_code>"><img src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>"> {% trans "<Language>" %}</a>
```
6. Don't forget to add a country's flag icon to `static/images/flags/`