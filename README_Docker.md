Docker commands to build and start server

Example info used:
https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application

From parent directory 'flydar'
```
docker build -t flydar .
```

```
docker run -it -p 8000:8000 flydar
```
