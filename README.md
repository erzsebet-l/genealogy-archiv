# Генеалогический архив

## Запуск проекта

### Требования (скачиваете)
- **Docker Desktop** — [скачать](https://www.docker.com/products/docker-desktop/)
- **Git** — [скачать](https://git-scm.com/downloads)

### Первый запуск
git clone https://github.com/ВАШ_ЛОГИН/genealogy-archive.git (просто ссылка репозитория)
cd genealogy-archive (переходите в папку проекта)
docker-compose up --build (при первом запуске происходит сборка)
docker-compose exec backend python manage.py migrate (в новом терминале)
docker-compose exec backend python manage.py createsuperuser (для админки, для удобства)
### Ежедневный запуск:
git pull origin main (получение измениний с репозитория)
docker-compose up (обычный запуск проекта без пересборки)
docker-compose exec backend python manage.py migrate   # если были изменения в моделях в бд
### Структура:
genealogy-archive/
├── backend/           # Django
├── frontend/          # Vue
└── docker-compose.yml # Запуск всех сервисов

### Git — краткий гайд
git pull origin main (получить измениния с репозитория)
git add . (добавить все измененные файлы для отправки)
git commit -m "Что сделали" (коммит)
git push origin main (отправка изменений на главную ветку main)
git checkout -b feature/название-задачи (создание ветки для новой задачи, feature-префикс, почитаете как создавать ветки)
git push origin feature/название-задачи (отправить ветку на гитхаб, будет подтверждение)
git status          (какие файлы изменены)
git log --oneline   (история коммитов)
git branch          (список веток)
