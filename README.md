# Генеалогический архив

## Запуск проекта

### Требования
- Docker Desktop

### Первый запуск
```bash
git clone https://github.com/ВАШ_ЛОГИН/genealogy-archive.git
cd genealogy-archive
docker-compose up --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser