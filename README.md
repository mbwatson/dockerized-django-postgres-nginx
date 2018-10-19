# Containerized Django App w/ Postgres (soon) served by Nginx

This is for running an existing Django project, although this repository contains the starter project created with `django-admin startproject`. Modifications to the project to align with common workflow situations are described below.

## Preparation

- Make sure your project already contains the directories referenced by the settings file--`media`, `static`, etc.
- Otherwise, Docker will create them, and they will be owned by root.
- Do the manage.py stuff in your environment--migrate, createsuperuser, collectstatic.

## Docker Compose

Two Docker Compose files exist here--one for development and one for production.

### Development

The development container simply serves the Django project via its builtin development server. Thus the `docker-compose.yml` file is small:

```
services:
  webapp:
    build:
      context: ./web/
      dockerfile: Dockerfile
    command: python3 ./web/manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/web
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=webapp.settings-dev
```

The build instructions come from the Dockerfile inside the project root, we start the development server on port 8000 (this is the default, so no surprise here), and we set the settings module to a development-specific settings module (more on this below).

### Production

The production situation is a little more involved. We start two (soon to be three) services: a server and our web application.

The webapp service is our Django project container, which is served via gunicorn by the command

```
command: gunicorn -w 4 webapp.wsgi:application -b 0.0.0.0:8000
```

Nginx will serve the static assets (as outlined in [the Django documentation](https://docs.djangoproject.com/en/2.1/howto/static-files/deployment/), so we mount those directories as separate volumes with

```
    volumes:
      - ./web/static_files:/web/static_files
      - ./web/media:/web/media
```

in the webapp service and the server service. The server service also mounts our nginx `.conf` file to replace the default Nginx `.conf` file.

```
    volumes:
      ...
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
```

## Project Requirements

Your Django project should reside in the `web` directory. One commonly uses either Pipenv or a requirements.txt file to define your project dependencies. Below describes how to proceed in either case. Note that if using one method, comment out the other.

### Using Pipenv?

Ensure your project has Pipfile and Pipfile.lock files, and make sure the following lines are uncommented in `web/Dockerfile`.

```
RUN pip3 install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
```

### Using requirement.txt?

Make sure the `requirements.txt` file resides in root of your Django project, and uncomment the following line in `web/Dockerfile`.

```
RUN pip install -r requirements.txt
```

Note that if you are using Pipenv, but still want to use a `requirements.txt` file, it can be generated with the `pipenv_to_requirements` module. Simply install the module with `pipenv install pipenv_to_requirements` and run `pipenv_to_requirements` in the environment (or `pipenv run pipenv_to_requirements` outside the environment).

## Django Settings

We often want to define settings modules for different environments (dev, prod, etc.), and this can be accomplished by creating additional settings files in the project root. The sample project in this repository already has this in place, but we'll describe here how to implement development- and production-specific settings in an existing project.

Create two files--`settings-dev.py` and `settings-prod.py`--in the project root. In these, we can define environment-specific variables, such as as Django's `SECRET_KEY` and `ALLOWED_HOSTS`.

In each new settings file, the base settings file, `settings.py`, should begin with a base settings import (i.e., the line `from .settings import *` at the top). The subsequent environment-specific definitions thereafter will add any necessary additional settings or overwrite definitions in the base settings file.

These settings files are referenced in the docker-compose files (depending on which is called when docker-compose is run) so the appropriate settings are loaded for your project.
Now we just tell docker-compose how to define the `DJANGO_SETTINGS_MODULE` environment variable so the appropriate settings file is used.

```
services:
  webapp:
    ...
    environment:
      - DJANGO_SETTINGS_MODULE=webapp.settings-prod
    ...
```

## Running the Containers

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sed vero explicabo dolorem dicta officia repellendus saepe non autem nemo eveniet ullam, qui fugit vitae iusto, sequi assumenda! Necessitatibus, vel, sapiente.

### Development

- `docker-compose up`

### Production

- `docker-compose -f docker-compose-prod.yml up`
