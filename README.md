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
```
5. In the project's settings `poetriumph/settings.py`, change the `DATABASES` variable to match your name of the `HOST` and `PORT`.
1. Create a superuser with `python manage.py createsuperuser`
1. Make migrations and migrate:
```
python manage.py makemigrations
python manage.py migrate
```
7. Set `DEBUG` to `False` before deploying to production.
8. Run server with `python manage.py runserver`
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