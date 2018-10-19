# Containerized Django App served by Nginx
(& soon with PostgreSQL)

## Summary

### What is Django?

Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

### What does this project accomplish?

This uses Docker-based scripts to deploy a multi-container Django 2.1 project (container 1) and serve with Nginx (container 2). Some details are outlined below.

- Python 3.7
- Django 2.1.2
- Pipenv virtual environment management
- (soon) PostgreSQL database
- Gunicorn for serving application
- Nginx for serving application and static files on separate volumes
- Assumes separated docker-compose environemt settings, with detailed instruction for achieving this workflow below.
- Can be run locally via Pipenv or with Docker Compose Docker

This project is for running an existing Django project, although this repository contains the starter project created with `django-admin startproject`. Modifications to the project to align with common workflow situations are described next. The base project already has migrations in place and a superuser (admin:misterios) to get up and running quickly.

## Preparing your Project

As mentioned above, this project comes packaged with the auto-generated Django project provided by `django-admin`. Beginning with this project, a more substantial project can be built. The more likely case is that you have an existing project, and you wish to drop it into this project. This section describes that process. Note that this walkthrough makes a few (reasonably common) assumptions about file locations and such.

Your Django project will live in the `./web` directory, and will henceforth be referred to as the project's root directory. Below, you'll see the structure of that directory.

```
$ tree ./web
.
├── assets
│   ├── css
│   ├── js
│   └── scss
├── db.sqlite3
├── Dockerfile
├── manage.py
├── media
├── Pipfile
├── Pipfile.lock
├── static_files
└── webapp
    ├── __init__.py
    ├── settings-dev.py
    ├── settings-prod.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Make sure your project already contains the directories referenced by the settings file--`media`, `static_files` in this case. Otherwise, they'll be created when Docker Compose creates its volumes, and they will be owned by root.

### Static Files

When your project is ready for deployment, your static files need to be collected. Django's settings file defines the locations related to this. This project assumes the configuration below.

```
# /web/webapp/settings.py

STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'assets'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

The `assets` directory is the location for static assets (`.css` and `.js` for example) during development.

In the project root (and in the virtual environment) `python manage.py collectstatic` packages these assets up into the `static_files` directory for production.

### Settings

The astute reader noticed several `settings*.py` files in the tree structure above. We define settings modules for different environments (in our case, one for development and one for production). These two additional settings files allows us to accomplish this. In these files, we define environment-specific variables, such as as Django's `SECRET_KEY` and `ALLOWED_HOSTS` variables.

The additional settings files each import the base settings file, `settings.py`, with `from .settings import *`. The environment-specific definitions thereafter will add any necessary settings or overwrite definitions in the base settings file.

These settings files are referenced in the `docker-compose` files so the appropriate settings are loaded for your project environment.

See below how we tell use docker-compose how to use these files for different situations.

## Running your Project

#### Dockerfile

The Dockerfile used to build the Django container takes care of installing your project's dependencies; here we outline two common options for this step. One commonly uses either Pipenv or a requirements.txt file to define your project dependencies.


```
# ./web/Dockerfile
FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /web
COPY . /web
WORKDIR /web

######################
###  Dependencies  ###
######################

# If using Pipenv...
RUN pip3 install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system

# If using requirements.txt file...
# RUN pip install -r requirements.txt

```

Below describes how to proceed in either case. Note that if using one method, delete or comment out the other.

### Using Pipenv?

Ensure your project has Pipfile and Pipfile.lock files, and make sure the following lines are uncommented in `web/Dockerfile`.

```
RUN pip3 install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
```

### Using requirements.txt?

Make sure the `requirements.txt` file resides in root of your Django project, and uncomment the following line in `web/Dockerfile`.

```
RUN pip install -r requirements.txt
```

\* Note that if you're using Pipenv and still want to use a `requirements.txt` file, it can be generated with the `pipenv_to_requirements` module. Simply install the module with `pipenv install pipenv_to_requirements` and run `pipenv_to_requirements` in the environment (or `pipenv run pipenv_to_requirements` outside the environment).

### Docker Compose

Two Docker Compose files exist here--one for development and one for production. Each references the corresponding Django settings module described above. Any additional Compose files would follow the same structure.

#### Development

Running `docker-compose up` spins up the development container, which simply serves the Django project via its builtin development server (as even the novice Django developer is used to doing without Docker). Thus the `docker-compose.yml` file is small:

```
# ./docker-compose.yml

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

There are few things happening here:

- the build instructions come from the `Dockerfile` inside the project root (detailed above);
- the development server starts, accessible on port 8000 (this is the default, so no surprise here);
- the entire project directory is mounted as a volume inside the container
- and we set the environment variable indicating that Django should use the development environment settings module.

### Production

The production situation is a little more involved but still quite simple. We start two (soon to be three) services: a server and our web application. Sping these containers up with `docker-compose -f docker-compose-prod.yml up`.

```
# ./docker-compose-prod.yml

version: '3'

volumes:
  static_files:
  media:
  conf:

services:
  webapp:
    container_name: webapp
    build:
      context: ./web/
      dockerfile: Dockerfile
    command: gunicorn -w 4 webapp.wsgi:application -b 0.0.0.0:8000
    volumes:
      - ./web/static_files:/web/static_files
      - ./web/media:/web/media
    ports:
      - 8000:8000
    environment:
      - DJANGO_SETTINGS_MODULE=webapp.settings-prod
  server:
    container_name: server
    image: nginx:latest
    ports:
      - 80:80
    volumes:
      - ./web/static_files:/web/static_files
      - ./web/media:/web/media
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - webapp

```

The webapp service is our Django project container, which is served via [Gunicorn](https://gunicorn.org/) by issuing the following command.

```
# ./docker-compose-prod.yml
    
    ...
    command: gunicorn -w 4 webapp.wsgi:application -b 0.0.0.0:8000
    ...
```

We also set an environment variable indicating that Django should use the production environment settings module.

```
# ./docker-compose-prod.yml
    
    ...
    environment:
      - DJANGO_SETTINGS_MODULE=webapp.settings-prod
    ...
```

Nginx will serve the static assets (as outlined in [the Django documentation](https://docs.djangoproject.com/en/2.1/howto/static-files/deployment/), so we mount those directories as separate volumes with

```
# ./docker-compose-prod.yml

    ...
    volumes:
      - ./web/static_files:/web/static_files
      - ./web/media:/web/media
    ...
```

in both the webapp and the server service. Additionally, the server also mounts our custom nginx configuration file `./nginx/default.conf` file to replace the default Nginx `.conf` file.

```
# ./docker-compose-prod.yml
        
    ...
    volumes:
      ...
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    ...
```

## Quickstart

### Dockerize Development

- `docker-compose up`

### Dockerize Production

- `docker-compose -f docker-compose-prod.yml up`

## Additional References

- Django: [https://docs.djangoproject.com/en/2.1/](https://docs.djangoproject.com/en/2.1/)
- Docker: [https://docs.docker.com](https://docs.docker.com)
- Docker Compose: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- Gunicorn: [https://gunicorn.org/](https://gunicorn.org/)
- Nginx: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)