# Loading fixtures

1. First enter django docker:

`docker-compose exec django bash`

2. Load the data

`
python manage.py loaddata <fixturename>
`

e.g. `python manage.py loaddata engines`