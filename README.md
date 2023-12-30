<div align = "center">

<img src="./static/images/logo_white.webp"></img>

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
DJANGO_SECRET_KEY="your_django_secret_key"
OPENAI_API_KEY="your_openai_api_key"

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=poetriumph
SQL_USER=poetriumph
SQL_PASSWORD="your_postgresql_password"
SQL_HOST=postgres
SQL_PORT=5432
PGDATA=/data/poetry-postgres
PG_CONTAINER_NAME=poetriumph-postgres

CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

WEB_CONTAINER_NAME=poetriumph
REDIS_CONTAINER_NAME=poetriumph-redis
CELERY_BEAT_CONTAINER_NAME=poetriumph-celery-beat
CELERY_WORKER_CONTAINER_NAME=poetriumph-celery-worker
WORKERS_RUNNING=1

EMAIL_FROM=example@gmail.com
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=some_password

# These are official recaptcha test keys which are used in development
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe

ALLOWED_HOSTS=127.0.0.1 localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1 http://localhost

DEBUG=1
```
* Create a `.env.dev` with the same values as `.env` except `SQL_HOST` and `WORKERS_RUNNING`:
```
SQL_HOST=localhost
WORKERS_RUNNING=

# You may remove these variables at all
```
`.env.dev` is utilized in conjunction with `docker-compose-lite.yml`, which includes only a PostgreSQL container with port 5432 exposed. The `WORKERS_RUNNING` environment variable is employed to skip tests involving Celery workers, such as sending emails during account activation.

> By default, `django-admin startproject` creates an insecure `SECRET_KEY` (see [Django docs](https://docs.djangoproject.com/en/5.0/ref/checks/#:~:text=connections%20to%20HTTPS.-,security.W009,-%3A%20Your%20SECRET_KEY%20has)). Generate a secure Django secret key for your project:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```


## Email Confirmation Upon Registration
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
* Build and start Docker containers with Redis, Celery, and PostgreSQL:
```
docker-compose up -d --build
```

> [!NOTE]  
> Celery [doesn't support](https://docs.celeryq.dev/en/stable/faq.html#does-celery-support-windows) Windows since version 4, so you can either run Celery in Docker containers (our case) or use a UNIX system to run each Celery process manually, each from a different terminal window:
```
celery -A poetriumph worker -l INFO
celery -A poetriumph beat -l INFO
```

* Make migrations and migrate:
```
python manage.py makemigrations && python manage.py migrate
```
* Load data for token types from a fixture:
```
python manage.py loaddata accounts/fixtures/token_types.json
``` 
* Create a super user:
```
python manage.py createsuperuser
```
* Manually create a profile for the super user:
```
python manage.py shell
```
```
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()
Profile.objects.create(user=User.objects.get(is_superuser=True))

exit()
```
* Collect all the static files into a single static directory:
```
python manage.py collectstatic
```
* Before deploying to production, set `DEBUG` to False in `.env` by not assigning any value to DEBUG:
```
DEBUG=
```
* If your `docker-compose.yml` is up, webserver will be available at `http://127.0.0.1:8008`
* If your `docker-compose-lite.yml` is up, start a development server:
```
python manage.py runserver
```


## Tests
Current code coverage is 98% (only Celery tasks are not tested). `coverage` tool is used to measure code coverage.
```
coverage run manage.py test
```
You will get correct results if you run `coverage` tool in `docker-compose.yml`'s web container:
```
docker-compose exec -it web bash
```
```
coverage run manage.py test
```
Additionally, to run tests faster, you can use `poetriumph.test_settings`. It includes a simpler password hashing algorithm:
```
coverage run manage.py test --settings=poetriumph.test_settings
```
Get a detailed report:
```
coverage report
```
Get annotated HTML listings with missed lines:
```
coverage html
```
Head to the created `htmlcov` folder and open `index.html` with `Live server`


## Add a New Language Interface
To use Django's localization, you need to install `GNU gettext tools` 0.15 or newer:
> [Question on Stack Overflow](https://stackoverflow.com/questions/35101850/cant-find-msguniq-make-sure-you-have-gnu-gettext-tools-0-15-or-newer-installed)
* Windows (choose `shared 64 bit` flavor):
> https://mlocati.github.io/articles/gettext-iconv-windows.html
* Linux:
```
sudo apt install gettext
```
* macOS:
```
brew install gettext

// Create symlink
brew link gettext --force
```

1. Add a folder for a new language:
```
django-admin makemessages -l <language-code>
```
For example, if you want to add French:
```
django-admin makemessages -l fr
```
> [Full list of languages and language codes (Wikipedia)](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

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
python manage.py compilemessages
```

5. Update `base.html` to add the new language to the dropdown menu. Replace `<lang_code>` and `<country>` with your language:
```html
...
{% elif request.LANGUAGE_CODE == '<language_code>' %}
<img class="image-flag me-1" src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>">Some Language
...
<a class="dropdown-item" href="/<lang_code>/{{ request.path|remove_language }}"><img class="image-flag me-1" src="{% static 'images/flags/<country>.png' %}" alt="flag_<country>">Some Language</a>
```