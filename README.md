### Django data

First enter django docker:

`docker-compose exec django bash`

You can create an admin user with these commands:

`python manage.py createsuperuser --username $DJANGO_ADMIN_USERNAME --email $DJANGO_ADMIN_EMAIL`

And enter your password of choice.

The React app requires an applications (uses django-oauth-toolkit)

`python manage.py createapplication --name searchapp confidential password`

In your browser, navigate to http://localhost:8000/admin/oauth2_provider/application/ Go to the detail page of the
searchapp app by clicking on it's id in the list of applications.

## django-docker.env configuration (back-end)

Make sure the values in the `django-docker.env` file are correct. To see which values must be present, use the example
template from `django-docker.env.sample`

## react.env configuration (front-end)

Make sure to change the settings in react.env to the correct values. The following keys must be present:

- `REACT_APP_API_URL`
- `REACT_APP_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`
- `REACT_DJANGO_CLIENT_ID`
- `REACT_DJANGO_CLIENT_SECRET`

### React App

If you want to run the React app locally without docker you can run the following command

`npm run start`

## Local development with npm run start

To configure this look at the `README.md` in the `/frontend` folder.
