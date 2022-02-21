docker compose up -d
docker-compose exec web python manage.py test --verbosity=1
