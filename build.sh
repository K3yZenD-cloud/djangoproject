#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@elixir.com', 'elixir2024')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "Build completed successfully!"
