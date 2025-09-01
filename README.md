# Habit Tracker — Бэкенд для трекера привычек

Курсовой проект по Django: бэкенд SPA-приложения для отслеживания полезных и приятных привычек с Telegram-уведомлениями.

## Возможности

- Регистрация и авторизация (JWT)
- CRUD привычек (полезных/приятных)
- Связанные привычки и награды
- Публичные привычки
- Ежедневные напоминания через Telegram-бота
- Асинхронные задачи через Celery + Redis
- Пагинация (по 5 привычек)
- Документация Swagger (drf-yasg)
- Тесты (pytest + покрытие)
- Переменные окружения (`.env`)
- Полное покрытие Flake8

# CW5 — Django DRF + Celery + Redis + Postgres + Nginx (Docker/Compose, CI/CD)

Проект: Django REST API с Celery задачами и Redis брокером/результатами.
Контейнеры: backend (gunicorn), celery_worker, celery_beat, postgres, redis, nginx.
Управление зависимостями — Poetry. Автодеплой — GitHub Actions → сервер.

## Технологии

- Python 3.12, Django 5, DRF
- Celery 5, Redis 7
- PostgreSQL 16
- gunicorn + Nginx
- Poetry
- Docker / Docker Compose
- GitHub Actions (CI: lint/test + build-check; CD: build&push GHCR → deploy)
## Быстрый старт локально (без Docker)
- Требуется PostgreSQL и Redis установленные локально.

1) Установить Poetry
pipx install poetry  # или: pip install --user poetry

2) Установить зависимости
poetry install

3) Создать .env в корне (см. пример ниже)
cp .env.example .env  # если есть .env.example, иначе создайте вручную

4) Миграции и суперпользователь
poetry run python manage.py migrate
poetry run python manage.py createsuperuser

5) Запуск dev-сервера
poetry run python manage.py runserver 0.0.0.0:8000

6) Celery (в отдельных окнах терминала):

poetry run celery -A config worker -l info -c 2
poetry run celery -A config beat -l info -S django

## Доступ:

Nginx: http://localhost:8080/

Swagger: http://localhost:8080/swagger/

Прямой backend (gunicorn): http://localhost:8000/


## Переменные окружения (.env)

Файл .env в корне проекта (для локального/CI) и на сервере (в ~/cw5/.env):

1) Django
SECRET_KEY=change-me-super-secret
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,backend,<ПУБЛИЧНЫЙ_IP_СЕРВЕРА>

2) Postgres
NAME=CW5
USER=postgres
PASSWORD=postgres
HOST=db        # локально через docker-compose (или 127.0.0.1 вне docker)
PORT=5432

3) Redis
REDIS_HOST=redis
REDIS_PORT=6379

4) Прочее
TZ=Asia/Tbilisi

## Скрипты контейнеров

В docker/entrypoint/:

- backend-entrypoint.sh — ожидание БД/Redis → миграции → collectstatic → запуск gunicorn.

- celery-worker-entrypoint.sh — worker.

- celery-beat-entrypoint.sh — beat (с django-celery-beat).

- docker/wait-for-it.sh — ожидание доступности host:port.

## Тесты и линтинг

### Конфиги:

.flake8 — исключает .venv, миграции; max-line-length=120.

pytest.ini — DJANGO_SETTINGS_MODULE=config.settings.

### Запуск локально:

poetry run flake8 .
poetry run pytest

## CI/CD (GitHub Actions)

### Workflow: .github/workflows/ci-cd.yml

- PR → develop/main:

    Lint & Test (Postgres/Redis поднимаются как services),

    Docker build (no push) — проверка, что образ собирается (без публикации).

- push → main (после merge):

    Build & Push образа в GHCR: ghcr.io/<owner>/<repo>/app:<sha>, latest

    Deploy на сервер по SSH: копирует docker-compose.prod.yml и nginx.conf, делает docker compose up -d.

### Secrets (Settings → Secrets and variables → Actions)

Обязательно добавить:

- PROD_HOST — публичный IP сервера (Yandex.Cloud).

- PROD_USER — SSH-логин на сервере (например, ubuntu).

- PROD_PATH — путь деплоя на сервере (например, /home/ubuntu/cw5).

- PROD_SSH_KEY — приватный SSH-ключ (полностью, с -----BEGIN ... END-----), парный к ключу в ~/.ssh/authorized_keys на сервере.

- GHCR_USERNAME — GitHub username (для логина в GHCR на сервере).

- GHCR_TOKEN — Personal Access Token (classic) с правом read:packages (если образы приватные).


## Подготовка сервера

### Ubuntu 22.04+/24.04, пользователь ubuntu (или свой). Команды выполнить на сервере:

1) Docker + Compose
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release; echo $UBUNTU_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

2) разрешить docker без sudo
sudo usermod -aG docker $USER

3) (опционально) файрволл
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable

4) каталог деплоя и .env
mkdir -p ~/cw5
nano ~/cw5/.env   # вставить переменные (см. раздел .env)


### SSH-ключ для Actions: публичную часть (из пары к PROD_SSH_KEY) добавить в ~/.ssh/authorized_keys:

mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-ed25519 AAAA... cw5-deploy" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

## Деплой

1. Смёрджить develop → main (или фичу → develop, затем develop → main).
2. Вкладка Actions: дождаться Build & Push → Deploy.
3. На сервере проверить:
    ssh ubuntu@<IP>
    cd ~/cw5
    docker compose -f docker-compose.prod.yml ps
    docker compose -f docker-compose.prod.yml logs -f backend
4. Открыть в браузере:
    http://<IP>/swagger/

## Пути и эндпоинты

- Swagger: /swagger/
- Статика: Nginx раздаёт из volume django_static на /static/.
- Медиа: /media/.

## Траблшутинг

- Permission denied (publickey) в Deploy
→ Пара ключей не совпадает. PROD_SSH_KEY (секрет) должен быть парой к ключу в ~/.ssh/authorized_keys на сервере. Проверь логин (PROD_USER), IP (PROD_HOST), путь (PROD_PATH).

- 401/unauthorized при login ghcr.io на сервере
→ Проверь GHCR_USERNAME и GHCR_TOKEN (read:packages). Если репо публичное, логин может не требоваться; если приватное — обязателен.

- Django 400 Bad Request после деплоя
→ Добавь публичный IP сервера в ALLOWED_HOSTS в .env на сервере.

- Порт 80 занят
→ Либо останови другой сервис, либо в docker-compose.prod.yml поменяй публикацию порта Nginx на "8080:80".

- Миграции не применяются
→ Смотри логи backend: docker compose -f docker-compose.prod.yml logs -f backend. В backend-entrypoint.sh миграции запускаются автоматически.

- CI: flake8 ругается на .venv/модули
→ В .flake8 исключены .venv, */migrations/*. Если запускаешь flake8 вручную — используй конфиг из репозитория.
