<div align = "center">

<img src="./static/images/logo_white.png"></img>

<p>Bridging Verses, Connecting Cultures</p>

</div>


## Description
Poetriumph is a Python/Django project to translate poems from one language to another and save them to the PostgreSQL database.


## Installation
* Create and activate a virtual environment:
```
python3 -m venv venv && source venv/bin/activate
```
* Install required dependencies:
```
python3 -m pip install -r requirements.txt
```
* Create a `.env` file in the root directory of your project. Add the following variables (replace values with your own):
```
SECRET_KEY="your_django_secret_key"
OPENAI_API_KEY="your_openai_api_key"

POSTGRES_DB=poetriumph
POSTGRES_USER=poetriumph
POSTGRES_PASSWORD="your_postgresql_password"
PGDATA=/data/davon-postgres
PG_CONTAINER_HOST=127.0.0.1
PG_CONTAINER_NAME=poetriumph-postgres

WEB_CONTAINER_NAME=poetriumph
REDIS_CONTAINER_NAME=poetriumph-redis

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
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
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
sudo docker volume create postgres_data_poetry
```
* Build and start Docker containers with the local services:
```
sudo docker-compose -f docker-compose-dev.yml up -d --build
```
* Make migrations and migrate:
```
python3 manage.py makemigrations && python3 manage.py migrate
```
* Create a super user:
```
python3 manage.py createsuperuser
```
* Manually create a profile for the super user:
```
python3 manage.py shell

from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()
Profile.objects.create(user=User.objects.get(is_superuser=True))

exit()
```
* Before deploying to production, set `DEBUG` to False in `.env` by not assigning any value to DEBUG:
```
DEBUG=
```
* Start a celery worker (used for sending activation emails in the background):
```
celery -A poetriumph.celery worker -l info
```
> [!NOTE]  
> Celery doesn't support Windows since [version 4](https://docs.celeryq.dev/en/stable/faq.html#does-celery-support-windows), so either use a UNIX system or use a different task queue.
* Start a development web server:
```
python3 manage.py runserver
```


## Add a New Language Interface
To use Django's localization, you need to install `GNU gettext tools` 0.15 or newer:
```
sudo apt install gettext
```
[How to install GNU on other platforms](https://stackoverflow.com/questions/35101850/cant-find-msguniq-make-sure-you-have-gnu-gettext-tools-0-15-or-newer-installed)

1. Add a folder for a new language:
```
django-admin makemessages -l <language-code>
```
For example, if you want to add French:
```
django-admin makemessages -l fr
```
[Full list of languages and language codes (Wikipedia)](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

2. Go to the file with translations:
```
locale/<language-code>/LC_MESSAGES/django.po
```
3. Fill the empty space of every `msgstr` with the translation. For example:
```
#: .\poetry_translation\config.py:4
msgid "Detect language"
msgstr "Détecter la langue"
```
4. Compile all translations:
```
python3 manage.py compilemessages
```
5. Update `base.html` to add the new language to the dropdown menu. Replace `<lang_code>` and `<country>` with your language:
```html
...
{% elif request.LANGUAGE_CODE == '<language_code>' %}
<img class="image-flag me-1" src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>">Some Language
...
<a class="dropdown-item" href="/<lang_code>/{{ request.path|remove_language }}"><img class="image-flag me-1" src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>">Some Language</a>
```