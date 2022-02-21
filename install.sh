echo "running docker build"
docker build .
echo "running docker compose up -d"
docker compose up -d
echo "django:makemigrations"
docker compose exec web python manage.py makemigrations
echo "django:migrate"
docker compose exec web python manage.py migrate
echo "creating superuser (admin)"
docker compose exec web python manage.py createsuperuser --username admin
echo "running tests"
docker compose exec web python manage.py test
