FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /src
COPY . /src
WORKDIR /src

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