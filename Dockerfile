# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py data_test
ENTRYPOINT [ "python", "manage.py", "runserver" ]