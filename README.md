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

## Технологии

- Python 3.12
- Django 5.2
- Django REST Framework
- drf-yasg
- Celery + Redis
- PostgreSQL (или SQLite)
- python-telegram-bot
- pytest
- black / isort / mypy  / flake8
