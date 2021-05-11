### Django data

First enter django docker:

`docker-compose exec django /bin/bash`

You can create an admin user with these commands:

`python manage.py createsuperuser --username $DJANGO_ADMIN_USERNAME --email $DJANGO_ADMIN_EMAIL`

And enter your password of choice.

### React App
If you want to run the React app locally without docker you can run the following command

`npm run start`