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

#  requirements.txt file
# RUN pip install -r requirements.txt
