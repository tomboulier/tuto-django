# Getting started with Django

This project is built by following [this tutorial](https://docs.djangoproject.com/en/4.1/intro/)
in the official webpage of [Django](https://www.djangoproject.com/).

## Installation
It is highly recommended to use a virtual environment, using Python version at least 3.8 and Django version at least 4.1:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

You can then create the database with the following command:

```
python manage.py migrate
```

## Usage

### Run the server

In the root folder, simply type:

```
python manage.py runserver
```

The app is then available at [http://127.0.0.1:8000/polls](http://127.0.0.1:8000/polls).

### Admin panel

The admin panel is available at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin). But before that, you
need to create an admin account with the following command:

```
python manage.py createsuperuser
```
