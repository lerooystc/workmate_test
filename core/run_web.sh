# Уменьшить после первой инициализации базы данных
sleep 30


cd core
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
