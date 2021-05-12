Shouldn't be needed:
`
cd backend/
`

`
python manage.py test tests.documents.test_models
`

# To get into postgres

`
docker-compose exec occ_postgres psql -U [POSTGRES_USER] -W [POSTGRES_USER] [POSTGRES_USER]
`

## In the container

All tables: `\dt`

Check table schema:` \d <table>`
