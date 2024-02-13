FROM python:3.7.17-slim-bullseye
RUN mkdir deployment
COPY . /deployment
WORKDIR /deployment/greenfield
RUN pip install install -r requirements.txt
EXPOSE 8080
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8080