# Containerized Django App w/ Postgres served by Nginx

This is for running an existing project

## Preparation

- Make sure your project already contains the directories referenced by the settings file--`media`, `static`, etc.
- Otherwise, Docker will create them, and they will be owned by root.
- Do the manage.py stuff in your environment--migrate, createsuperuser, collectstatic.

## Project Requirements

- place `requirements.txt` in root of django project, djangoproject
- if using pipenv, requirements file can be generated with the `pipenv_to-requirements` module

## Settings

we'll define settings files for different environments here.

- Move the default Django settings file (`djangoproject/settings.py`) to `djangoproject/settings/base.py`
- Define development- and production-specific settings in `settings/development.py` and `settings/production.py`, respectively, such as `SECRET_KEY` and `ALLOWED_HOSTS`.
- These settings files are defined in the docker-compose files (depending on which is called when docker-compose is run) so the appropriate settings are loaded for your project.
- Each of these files will import the base settings, which now live in `settings/base.py`, and overwrite anything defined in them.

## Running the Containers

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sed vero explicabo dolorem dicta officia repellendus saepe non autem nemo eveniet ullam, qui fugit vitae iusto, sequi assumenda! Necessitatibus, vel, sapiente.

### Development

- `docker-compose up`

### Production

- `docker-compose -f docker-compose-prod.yml up`
