
# Генеалогический архив

### Запуск проекта

- **Docker Desktop** — [скачать](https://www.docker.com/products/docker-desktop/) 
- **Git** — [скачать](https://git-scm.com/downloads)

### Первый запуск

```bash
git clone https://github.com/ВАШ_ЛОГИН/genealogy-archive.git #ссылка на репозиторий
cd genealogy-archive
docker-compose up --build #запуск со сборкой
```

**В новом терминале (терминал с запущенным проектом не закрывать):**
```bash
docker-compose exec backend python manage.py migrate #приминение миграций (таблицы бд)
docker-compose exec backend python manage.py createsuperuser #создание админа для удобства (не обязательно)
```

### Ежедневный запуск

```bash
git pull origin main #получение изменений с репозитория
docker-compose up #запуск без пересборки
docker-compose exec backend python manage.py migrate   # если были изменения в моделях
```

### Структура

```
genealogy-archive/
├── backend/           # Django
├── frontend/          # Vue
└── docker-compose.yml # Запуск всех сервисов
```

### Git — краткий гайд

| Команда | Что делает |
|---------|------------|
| `git pull origin main` | Получить изменения с репозитория |
| `git add .` | Добавить все изменённые файлы |
| `git commit -m "Что сделали"` | Сохранить изменения локально |
| `git push origin main` | Отправить изменения на GitHub |

**Ветки:**
```bash
git checkout -b feature/название-задачи   # создать ветку
git push origin feature/название-задачи   # отправить ветку на GitHub
# затем на GitHub создать Pull Request
```

**Проверка статуса:**
```bash
git status          # какие файлы изменены
git log --oneline   # история коммитов
git branch          # список веток
```
