# README for Poetorium Django Project
Poetorium is a Django project that allows users to translate poems from one language to another and save them to the PostgreSQL database.
## Installation
1. Create a virtual environment with `python -m venv venv`
1. Activate the virtual environment with `venv\scripts\activate`
1. Install required dependencies with `python -m pip install -r requirements.txt`
1. Create a `.env` file which contains environment variables in the root directory of your project. Add the following variables:
```
SECRET_KEY="your_django_secret_key"
OPEN_API_KEY="your_openai_api_key"
psql_db="name_of_postgresql_database"
postgres_user="your_postgresql_username"
postgres_password="your_postgresql_password"
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
