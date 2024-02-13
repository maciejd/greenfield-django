# greenfield-django
Test management app using Django, SQLite and Bootstrap (with 100% test coverage)

1. Clone repo `git clone https://github.com/maciejd/greenfield-django.git`

2. Chande directory `cd greenfield-django`

3. Build image `docker build -t greenfield .` 
  
4. Run container in detached mode and publish port 8080 `docker run -d -p 8080:8080 greenfield`

5. Connect to the container shell and execute `python manage.py createsuperuser` to create your user
  
5. App should be accessible on port 8080 `http://localhost:8080/greenfield/suite`(will redirect to login)

![alt text](http://i.imgur.com/a8N1o8P.png "Greenfield Report List")
