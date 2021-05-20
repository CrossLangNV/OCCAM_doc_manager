### Django data

First enter django docker:

`docker-compose exec django /bin/bash`

You can create an admin user with these commands:

`python manage.py createsuperuser --username $DJANGO_ADMIN_USERNAME --email $DJANGO_ADMIN_EMAIL`

And enter your password of choice.

The React app requires an applications (uses django-oauth-toolkit)

`python manage.py createapplication --name searchapp confidential password`

In your browser, navigate to http://localhost:8000/admin/oauth2_provider/application/ Go to the detail page of the
searchapp app by clicking on it's id in the list of applications. In the user field, add the admin user.

Also check that the "Client id" and the "Client secret" match with the values in secrets/django-docker.env:

`REACT_DJANGO_CLIENT_ID= `

`REACT_DJANGO_CLIENT_SECRET=`

### React App

If you want to run the React app locally without docker you can run the following command

`npm run start`