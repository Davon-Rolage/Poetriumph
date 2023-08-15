# README for Poetorium Django Project
Poetorium is a Django project that allows users to translate poems from one language to another and save them to database.<br>
It uses PostgreSQL database.
## Installation
1. Create a virtual environment with `python -m venv venv`
1. Activate the virtual environment with `venv\scripts\activate`
1. Install required dependencies with `python -m pip install -r requirements.txt`
1. Create a `.env` file which contains environment variables in the root directory of your project. Add the following variables:
```
SECRET_KEY=<your_django_secret_key>
OPEN_API_KEY=<your_openai_api_key>
psql_db=<name_of_postgresql_database>
postgres_user=<your_postgresql_username>
postgres_password=<your_postgresql_password>
```
5. In the project's settings `poetriumph/settings.py`, change the `DATABASES` variable to match your name of the `HOST` and `PORT`.
1. Make migrations and migrate:
```
python manage.py makemigrations
python manage.py migrate
```
7. Set `DEBUG` to `False` before deploying to production.
8. Run server:
```
python manage.py runserver
```

## Premium Feature Implementation
To implement premium features for users, follow these steps:
1. Go to `\venv\Lib\site-packages\django\contrib\auth\models.py`, find the `UserManager` class and the `create_user` method (not `_create_user`!).
1. Add `is_premium` attribute and set it to `False` for a user:
```python
extra_fields.setdefault("is_superuser", False)
extra_fields.setdefault("is_premium", False) # add this line
```
3. Do the same with the superuser, but set `is_premium` to `True`:
```python
extra_fields.setdefault("is_superuser", True)
extra_fields.setdefault("is_premium", True) # add this line
```
4. Find the `AbstractUser` class and add the `is_premium` field after the `is_active` field:
```python
is_premium = models.BooleanField(
     _("premium"),
     default=False,
     help_text=_(
         "Designates whether this user is a premium user. "
     )
 )
```
5. Find the `AnonymousUser` class and add the `is_premium` attribute to it set to `False`:
```python
is_active = False
is_premium = False # add this line
is_superuser = False
```
6. Go to `\venv\Lib\site-packages\django\contrib\auth\admin.py`, find the `UserAdmin` class and add the `is_premium` field to the `fieldsets` variable:
```python
{
    "fields": (
        "is_premium", # add this line
        "is_active",
        ...
    ),
},
```
7. In the same class, find the `list_display` variable and add the `is_premium` field to the end. Do the same with the `list_filter` variable.

### Now you can manage user premium features from the Admin Panel. If you have any questions or issues, feel free to contact us.
