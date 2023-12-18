<div align = "center">

<img src="./static/images/logo_white.png"></img>

<p>Bridging Verses, Connecting Cultures</p>

</div>


## Description
Poetriumph is a Python/Django project to translate poems from one language to another and save them to the PostgreSQL database.


## Installation
* Create and activate a virtual environment:
```
python -m venv venv && venv\Scripts\activate
```
* Install required dependencies:
```
python -m pip install -r requirements.txt
```
* Create a `.env` file in the root directory of your project. Add the following variables (replace values with your own):
```
SECRET_KEY="your_django_secret_key"
OPENAI_API_KEY="your_openai_api_key"

POSTGRES_DB=poetriumph
POSTGRES_USER=poetriumph
POSTGRES_PASSWORD="your_postgresql_password"
PG_CONTAINER_HOST=127.0.0.1
PG_CONTAINER_NAME=poetriumph-postgres

REDIS_CONTAINER_NAME=poetriumph-redis
WEB_CONTAINER_NAME=poetriumph
PGDATA=/data/davon-postgres

EMAIL_FROM=example@gmail.com
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=some_password

# These are recaptcha test keys which are used in development
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe

ALLOWED_HOSTS=127.0.0.1 localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1

DEBUG=1
```
> By default, `django-admin startproject` creates an insecure `SECRET_KEY` (see [Django docs](https://docs.djangoproject.com/en/5.0/ref/checks/#:~:text=connections%20to%20HTTPS.-,security.W009,-%3A%20Your%20SECRET_KEY%20has)). Generate a secure django secret key for your project:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```


## Email Confirmation upon registration
1. Go to [https://myaccount.google.com](https://myaccount.google.com) -> `Security` -> `2-Step Verification` (it has to be `ON`) -> `App passwords`
2. Create a new app name and put the shown password to `EMAIL_HOST_PASSWORD` variable in `.env`


## reCAPTCHA implementation
1. Go to [https://www.google.com/recaptcha/admin/create](https://www.google.com/recaptcha/admin/create)
1. Press `Switch to create a classic key`
1. Create a label, select `reCAPTCHA v2` and `"I'm not a robot" Checkbox`
1. Add a domain, e.g. `mysite.com` or `127.0.0.1` (localhost).
1. Accept their Terms of Service and press `Submit`
1. Copy `Site Key` to `RECAPTCHA_PUBLIC_KEY` variable in `.env`
1. Copy `Secret Key` to `RECAPTCHA_PRIVATE_KEY` variable in `.env`
___
* Create a docker volume:
```
docker volume create postgres_data_poetry
```
* Build and start a Docker container with the local services:
```
docker-compose -f docker-compose-dev.yml up -d --build
```
* Make migrations and migrate:
```
python manage.py makemigrations && python manage.py migrate
```
* Create a super user:
```
python manage.py createsuperuser
```
* Before deploying to production, set `DEBUG` to `False` in `.env` by not assigning any value to DEBUG:
```
DEBUG=
```
* Start a local development web server:
```
python manage.py runserver
```


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