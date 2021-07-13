To clear test database:
`
cat <(echo "yes") - | python manage.py test tests.documents.test_models.DocumentTest
`

When it complains about the folder:
`
cd backend/
`

# To get into postgres

`
docker-compose exec occ_postgres psql -U [POSTGRES_USER] -W [POSTGRES_USER] [POSTGRES_USER]
`

## In the container

All tables: `\dt`

Check table schema:` \d <table>`
